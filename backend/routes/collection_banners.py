import os
import time
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import cloudinary.uploader
from backend.extensions import db
from backend.models.collection import CollectionModel
from backend.models.collection_banner import CollectionBanner
from backend.middleware.auth import admin_required
from backend.utils.audit import log_admin_action

collection_banners_bp = Blueprint('collection_banners', __name__)

# Cloudinary Setup
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

if all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    try:
        import cloudinary
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET
        )
        CLOUDINARY_ENABLED = True
    except Exception:
        CLOUDINARY_ENABLED = False
else:
    CLOUDINARY_ENABLED = False

# Local Upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 1. Public/Admin route: Get all collection banners
@collection_banners_bp.route('', methods=['GET'])
@collection_banners_bp.route('/', methods=['GET'])
def get_all_collection_banners():
    try:
        banners = CollectionBanner.query.order_by(CollectionBanner.display_order.asc(), CollectionBanner.id.desc()).all()
        return jsonify([b.to_dict() for b in banners]), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching collection banners: {str(e)}"}), 500


# 2. Public/Admin route: Get single Collection Banner by primary key ID
@collection_banners_bp.route('/<int:id>', methods=['GET'])
def get_collection_banner_by_id(id):
    try:
        cb = CollectionBanner.query.get(id)
        if not cb:
            return jsonify({"message": f"Collection banner with ID {id} not found."}), 404
        return jsonify(cb.to_dict()), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching collection banner: {str(e)}"}), 500


# 3. Public route: Get dynamic Collection Banner by Collection (ID, Name, or Slug)
@collection_banners_bp.route('/by-collection/<path:collection_identifier>', methods=['GET'])
@collection_banners_bp.route('/collection/<path:collection_identifier>', methods=['GET'])
@collection_banners_bp.route('/<path:collection_identifier>', methods=['GET'])
def get_banner_by_collection(collection_identifier):
    try:
        collection_identifier = collection_identifier.strip()

        # Strip 'by-collection/' or 'collection/' prefix if present
        if collection_identifier.lower().startswith('by-collection/'):
            collection_identifier = collection_identifier[14:].strip()
        elif collection_identifier.lower().startswith('collection/'):
            collection_identifier = collection_identifier[11:].strip()

        collection = None

        # Try finding by numeric collection ID first
        if collection_identifier.isdigit():
            collection = CollectionModel.query.get(int(collection_identifier))

        # If not found by collection ID, check if it is a collection banner ID
        if not collection and collection_identifier.isdigit():
            cb = CollectionBanner.query.get(int(collection_identifier))
            if cb:
                return jsonify({
                    "banner": cb.to_dict(),
                    "collection_id": cb.collection_id,
                    "collection_name": cb.collection.name if cb.collection else ""
                }), 200

        # Find by name or slug (case-insensitive)
        if not collection:
            collection = CollectionModel.query.filter(
                (CollectionModel.name.ilike(collection_identifier)) |
                (CollectionModel.slug.ilike(collection_identifier))
            ).first()

        if not collection:
            return jsonify({
                "banner": None,
                "message": f"Collection '{collection_identifier}' not found."
            }), 200

        # Fetch only ACTIVE banner for this collection
        banner = CollectionBanner.query.filter_by(collection_id=collection.id, is_active=True).first()

        if not banner:
            return jsonify({
                "banner": None,
                "collection_id": collection.id,
                "collection_name": collection.name,
                "message": "No active banner for this collection."
            }), 200

        return jsonify({
            "banner": banner.to_dict(),
            "collection_id": collection.id,
            "collection_name": collection.name
        }), 200

    except Exception as e:
        return jsonify({"message": f"Error fetching collection banner: {str(e)}"}), 500



# 3. Admin route: Upload Collection Banner image
@collection_banners_bp.route('/upload', methods=['POST'])
@admin_required
def upload_collection_banner_image():
    if 'image' not in request.files:
        return jsonify({"message": "No image file provided."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"message": "No file selected."}), 400

    if CLOUDINARY_ENABLED:
        try:
            upload_result = cloudinary.uploader.upload(file)
            url = upload_result.get("secure_url")
            log_admin_action("Image Uploaded", "Site Configurations", f"Uploaded collection banner image to Cloudinary: {url}")
            return jsonify({
                "message": "Collection banner image uploaded to Cloudinary successfully!",
                "url": url
            }), 200
        except Exception as e:
            print(f"[CLOUDINARY] Upload failed, falling back to local: {e}")

    # Local storage fallback
    try:
        filename = secure_filename(file.filename)
        filename = f"coll_banner_{int(time.time())}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        url = f"/static/uploads/{filename}"
        log_admin_action("Image Uploaded", "Site Configurations", f"Uploaded collection banner image locally: {url}")
        return jsonify({
            "message": "Collection banner image uploaded locally successfully!",
            "url": url
        }), 200
    except Exception as ex:
        return jsonify({"message": f"Failed to upload collection banner image: {str(ex)}"}), 500


# 4. Admin route: Create or replace Collection Banner
@collection_banners_bp.route('', methods=['POST'])
@admin_required
def create_collection_banner():
    try:
        data = request.get_json() or {}

        collection_id = data.get("collection_id")
        banner_image = data.get("banner_image")

        if not collection_id:
            return jsonify({"message": "collection_id is required."}), 400
        if not banner_image or not str(banner_image).strip():
            return jsonify({"message": "banner_image is required."}), 400

        banner_image = str(banner_image).strip()

        collection = CollectionModel.query.get(collection_id)
        if not collection:
            return jsonify({"message": "Selected collection does not exist."}), 404

        # Validation: Only one active banner per collection. If existing banner exists, update or replace.
        banner = CollectionBanner.query.filter_by(collection_id=collection_id).first()

        status_val = data.get("status")
        is_active = bool(data.get("is_active", True))
        if status_val is not None:
            is_active = (str(status_val).lower() in ['active', 'true', '1'])

        is_new = banner is None

        if banner:
            # Update existing banner
            banner.banner_image = banner_image
            banner.title = data.get("title", "")
            banner.subtitle = data.get("subtitle", "")
            banner.description = data.get("description", "")
            banner.button_text = data.get("button_text", "")
            banner.button_link = data.get("button_link", "")
            banner.is_active = is_active
            banner.display_order = int(data.get("display_order", 0))
            action_event = "Banner Updated"
            action_desc = f"Updated collection banner for '{collection.name}'"
        else:
            # Create new banner
            banner = CollectionBanner(
                collection_id=collection_id,
                banner_image=banner_image,
                title=data.get("title", ""),
                subtitle=data.get("subtitle", ""),
                description=data.get("description", ""),
                button_text=data.get("button_text", ""),
                button_link=data.get("button_link", ""),
                is_active=is_active,
                display_order=int(data.get("display_order", 0))
            )
            db.session.add(banner)
            action_event = "Banner Created"
            action_desc = f"Created collection banner for '{collection.name}'"

        db.session.commit()

        log_admin_action(action_event, "Site Configurations", action_desc)
        if banner_image.startswith("http"):
            log_admin_action("Image URL Saved", "Site Configurations", f"Saved remote image URL for '{collection.name}': {banner_image}")

        return jsonify({
            "message": "Collection banner saved successfully!",
            "banner": banner.to_dict()
        }), 201 if is_new else 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error saving collection banner: {str(e)}"}), 500


# 5. Admin route: Update existing Collection Banner by ID
@collection_banners_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_collection_banner(id):
    try:
        banner = CollectionBanner.query.get(id)
        if not banner:
            return jsonify({"message": "Collection banner not found."}), 404

        data = request.get_json() or {}

        if "collection_id" in data and data["collection_id"] != banner.collection_id:
            new_coll_id = data["collection_id"]
            coll = CollectionModel.query.get(new_coll_id)
            if not coll:
                return jsonify({"message": "Selected collection does not exist."}), 404

            # Check for duplicate
            existing = CollectionBanner.query.filter_by(collection_id=new_coll_id).first()
            if existing and existing.id != banner.id:
                return jsonify({"message": f"A banner already exists for collection '{coll.name}'."}), 400
            banner.collection_id = new_coll_id

        if "banner_image" in data:
            banner.banner_image = str(data["banner_image"]).strip()
        if "title" in data:
            banner.title = data["title"]
        if "subtitle" in data:
            banner.subtitle = data["subtitle"]
        if "description" in data:
            banner.description = data["description"]
        if "button_text" in data:
            banner.button_text = data["button_text"]
        if "button_link" in data:
            banner.button_link = data["button_link"]
        if "display_order" in data:
            banner.display_order = int(data["display_order"])

        if "is_active" in data:
            banner.is_active = bool(data["is_active"])
        elif "status" in data:
            banner.is_active = (str(data["status"]).lower() in ['active', 'true', '1'])

        db.session.commit()

        coll_name = banner.collection.name if banner.collection else f"ID {banner.collection_id}"
        log_admin_action("Banner Updated", "Site Configurations", f"Updated collection banner for '{coll_name}'")

        return jsonify({
            "message": "Collection banner updated successfully!",
            "banner": banner.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating collection banner: {str(e)}"}), 500


# 6. Admin route: Toggle status (Active / Inactive)
@collection_banners_bp.route('/<int:id>/status', methods=['PATCH'])
@admin_required
def toggle_collection_banner_status(id):
    try:
        banner = CollectionBanner.query.get(id)
        if not banner:
            return jsonify({"message": "Collection banner not found."}), 404

        data = request.get_json(silent=True) or {}
        if "is_active" in data:
            banner.is_active = bool(data["is_active"])
        elif "status" in data:
            banner.is_active = (str(data["status"]).lower() in ['active', 'true', '1'])
        else:
            banner.is_active = not banner.is_active

        db.session.commit()

        coll_name = banner.collection.name if banner.collection else f"ID {banner.collection_id}"
        action_event = "Banner Activated" if banner.is_active else "Banner Disabled"
        log_admin_action(action_event, "Site Configurations", f"Toggled banner status for '{coll_name}' to {'Active' if banner.is_active else 'Inactive'}")

        return jsonify({
            "message": f"Banner status updated to {'Active' if banner.is_active else 'Inactive'}.",
            "banner": banner.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error toggling status: {str(e)}"}), 500


# 7. Admin route: Delete Collection Banner
@collection_banners_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_collection_banner(id):
    try:
        banner = CollectionBanner.query.get(id)
        if not banner:
            return jsonify({"message": "Collection banner not found."}), 404

        coll_name = banner.collection.name if banner.collection else f"ID {banner.collection_id}"
        db.session.delete(banner)
        db.session.commit()

        log_admin_action("Banner Deleted", "Site Configurations", f"Deleted collection banner for '{coll_name}'")

        return jsonify({"message": "Collection banner deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting collection banner: {str(e)}"}), 500
