from functools import wraps
import os
import logging
from flask import request, jsonify
import jwt
from backend.models.user import UserModel
from backend.models.admin import AdminModel
from backend.config import Config

JWT_SECRET = Config.JWT_SECRET

logger = logging.getLogger(__name__)

def is_admin_role(data):
    """
    Utility function to flexibly check if token payload or user object represents an Admin account.
    Handles boolean, integer, or case-insensitive string values for 'is_admin' and 'role'.
    """
    if not data or not isinstance(data, dict):
        return False
    
    # Check boolean or truthy is_admin flag
    is_admin_flag = data.get("is_admin")
    if is_admin_flag is True or str(is_admin_flag).strip().lower() in ("true", "1", "yes"):
        return True
        
    # Check role string (case-insensitive)
    role = str(data.get("role") or "").strip().lower()
    if role in ("admin", "superadmin", "super_admin", "super admin", "owner", "master"):
        return True
        
    return False

def extract_bearer_token():
    """
    Extract Bearer token from request headers cleanly.
    Filters out invalid string literals like 'null' or 'undefined'.
    """
    auth_header = request.headers.get('Authorization') or request.headers.get('authorization')
    if not auth_header:
        return None
    
    auth_header = str(auth_header).strip()
    if auth_header.lower().startswith('bearer '):
        token = auth_header[7:].strip()
        if token and token.lower() not in ("null", "undefined", "none", "\"null\"", "\"undefined\""):
            return token
    elif auth_header and auth_header.lower() not in ("null", "undefined", "none", "\"null\"", "\"undefined\""):
        # Allow raw token if Bearer prefix was omitted
        return auth_header
    return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return f(None, *args, **kwargs)
            
        token = extract_bearer_token()
        if not token:
            logger.warning("[AUTH_401] Token missing for endpoint=%s path=%s", request.endpoint, request.path)
            return jsonify({"message": "Authentication token is missing!"}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logger.warning("[AUTH_401] Expired token for endpoint=%s path=%s", request.endpoint, request.path)
            return jsonify({"message": "Token has expired! Please login again."}), 401
        except jwt.InvalidTokenError as e:
            logger.warning("[AUTH_401] Invalid token for endpoint=%s path=%s error=%s", request.endpoint, request.path, str(e))
            return jsonify({"message": "Invalid token! Please login again."}), 401
        except Exception as e:
            logger.error("[AUTH_401] Token decode error for endpoint=%s path=%s error=%s", request.endpoint, request.path, str(e))
            return jsonify({"message": f"Authentication error: {str(e)}"}), 401

        user_id = data.get("user_id") or data.get("admin_id") or data.get("id")
        
        if is_admin_role(data):
            admin_obj = None
            if user_id and str(user_id).isdigit():
                admin_obj = AdminModel.query.get(int(user_id))
            if not admin_obj and data.get("username"):
                admin_obj = AdminModel.query.filter_by(username=data.get("username")).first()
            if not admin_obj and data.get("email"):
                admin_obj = AdminModel.query.filter_by(email=data.get("email")).first()
            if not admin_obj:
                admin_obj = AdminModel.query.first()

            if admin_obj:
                current_user = {
                    "_id": str(admin_obj.id),
                    "id": str(admin_obj.id),
                    "name": admin_obj.username,
                    "username": admin_obj.username,
                    "email": admin_obj.email or (admin_obj.username if "@" in admin_obj.username else f"{admin_obj.username}@admin.local"),
                    "is_admin": True,
                    "role": "admin"
                }
            else:
                current_user = {
                    "_id": str(user_id or "1"),
                    "id": str(user_id or "1"),
                    "name": data.get("username") or data.get("name") or "Administrator",
                    "email": data.get("email") or "admin@admin.local",
                    "is_admin": True,
                    "role": "admin"
                }
        else:
            current_user = UserModel.find_by_id(user_id) if user_id else None
            
        if not current_user:
            logger.warning("[AUTH_401] User/Admin not found for endpoint=%s user_id=%s", request.endpoint, user_id)
            return jsonify({"message": "User not found or disabled!"}), 401

        if isinstance(current_user, dict) and current_user.get("is_blocked"):
            logger.warning("[AUTH_403] Blocked user attempt endpoint=%s user_id=%s", request.endpoint, user_id)
            return jsonify({"message": "Your account has been suspended by the administrator."}), 403

        return f(current_user, *args, **kwargs)
        
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)
            
        token = extract_bearer_token()
        if not token:
            logger.warning("[ADMIN_AUTH_401] Bearer token missing for endpoint=%s path=%s", request.endpoint, request.path)
            return jsonify({"message": "Authentication token is missing!"}), 401
            
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logger.warning("[ADMIN_AUTH_401] Expired admin token for endpoint=%s path=%s", request.endpoint, request.path)
            return jsonify({"message": "Admin session expired. Please log in again."}), 401
        except jwt.InvalidTokenError as e:
            logger.warning("[ADMIN_AUTH_401] Invalid admin token for endpoint=%s path=%s error=%s", request.endpoint, request.path, str(e))
            return jsonify({"message": f"Access denied! Invalid authentication token ({str(e)})."}), 401
        except Exception as e:
            logger.error("[ADMIN_AUTH_401] Decode error for endpoint=%s path=%s error=%s", request.endpoint, request.path, str(e))
            return jsonify({"message": f"Access denied! Invalid authentication token ({str(e)})."}), 401

        user_id = data.get("user_id") or data.get("admin_id") or data.get("id")

        # 1. Level 1: JWT payload explicitly contains admin privileges
        if is_admin_role(data):
            logger.info("[ADMIN_AUTH_SUCCESS] Admin authorized via payload flag for endpoint=%s path=%s user_id=%s", request.endpoint, request.path, user_id)
            return f(*args, **kwargs)

        # 2. Level 2: Query AdminModel database table
        admin_obj = None
        if user_id and str(user_id).isdigit():
            admin_obj = AdminModel.query.get(int(user_id))
        if not admin_obj and data.get("username"):
            admin_obj = AdminModel.query.filter_by(username=data.get("username")).first()
            
        if admin_obj:
            logger.info("[ADMIN_AUTH_SUCCESS] Admin authorized via AdminModel for endpoint=%s path=%s admin_id=%s", request.endpoint, request.path, admin_obj.id)
            return f(*args, **kwargs)

        # 3. Level 3: Query UserModel database table for is_admin flag or admin role
        if user_id:
            current_user = UserModel.find_by_id(user_id)
            if current_user and is_admin_role(current_user):
                logger.info("[ADMIN_AUTH_SUCCESS] Admin authorized via UserModel for endpoint=%s path=%s user_id=%s", request.endpoint, request.path, user_id)
                return f(*args, **kwargs)

        logger.warning("[ADMIN_AUTH_DENIED_403] 403 Forbidden for endpoint=%s path=%s user_id=%s payload=%s", request.endpoint, request.path, user_id, data)
        return jsonify({"message": "Access denied! Admin privileges required."}), 403
        
    return decorated
