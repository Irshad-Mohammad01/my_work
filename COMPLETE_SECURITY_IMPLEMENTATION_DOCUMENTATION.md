# SSJewellery — Complete Security Implementation & Architecture Documentation

This document provides complete, end-to-end technical documentation of the security, encryption, credential hashing, and authentication architecture implemented across the **SSJewellery** web platform (Backend Flask & Neon DB PostgreSQL).

---

## Executive Security Summary

| Domain | Security Component | Mechanism / Algorithm | Storage / Prefix Format | Reversibility |
| :--- | :--- | :--- | :--- | :--- |
| **Passwords** | User & Admin Credentials | **Bcrypt** (Salted Blowfish, 12 rounds) | `$2b$12$...` / `$2a$12$...` | **Irreversible** (One-Way Hash) |
| **Admin Identity** | `admins.username` | **AES-256-CBC** (`EncryptedString`) | `BB_ENC:<Base64(IV + Ciphertext)>` | **Reversible** (Two-Way Encryption) |
| **Customer PII** | `users.full_name`, `users.email`, `users.phone` | **AES-256-CBC** (`EncryptedString`) | `BB_ENC:<Base64(IV + Ciphertext)>` | **Reversible** (Two-Way Encryption) |
| **Delivery Addresses** | `delivery_addresses` columns | **AES-256-CBC** (`EncryptedString`) | `BB_ENC:<Base64(IV + Ciphertext)>` | **Reversible** (Two-Way Encryption) |
| **Session Security** | API Tokens & Authorization | **JWT (HS256)** | `Bearer <JWT_TOKEN>` | Standard Signed Claims |
| **Brute-Force Protection** | Login & OTP Rate Limiting | `UserAttempt` Lockout Engine | In-Database Lock Tracking | 15-Minute Auto-Release |
| **Audit Compliance** | System Security Logs | `AdminAuditLog` | Structured PostgreSQL Records | Read-Only Audit History |

---

## 1. Data Encryption at Rest (AES-256-CBC)

### Architecture Location
- **Module**: `backend/utils/security.py`
- **ORM Class**: `EncryptedString` (SQLAlchemy `TypeDecorator`)

### Technical Encryption Flow
```
 Plaintext String ("admin" or "user@domain.com")
                         │
                         ▼
           16-Byte Deterministic IV
   IV = SHA-256(Plaintext).digest()[:16]
                         │
                         ▼
        AES-256-CBC Cipher (PKCS7 Padded)
                         │
                         ▼
     Combine [16-Byte IV + Encrypted Ciphertext]
                         │
                         ▼
                  Base64 Encoding
                         │
                         ▼
       Database Storage Output: "BB_ENC:<Base64>"
```

### Deterministic Synthetic IV Design Rationale
- **Deterministic Lookup**: Standard random IVs make exact SQL matching impossible (`WHERE username = '...'`). By synthesizing a 16-byte IV deterministically from the SHA-256 digest of the plaintext, identical inputs produce identical `BB_ENC:...` values.
- **SQL Efficiency**: Allows seamless indexed query matching (`AdminModel.username == admin_identifier`) without decrypting all database rows.

### Transparent ORM Lifecycle (`EncryptedString`)
- **On Save (`process_bind_param`)**: Automatically converts plaintext inputs into `BB_ENC:...` before sending SQL `INSERT` / `UPDATE` queries to Neon DB.
- **On Read (`process_result_value`)**: Detects `BB_ENC:` prefix on SQL result sets, automatically decrypts ciphertext, and yields original unencrypted strings in Flask runtime memory.

---

## 2. One-Way Credential Hashing (Bcrypt)

### Architecture Location
- **Modules**: `backend/models/user.py`, `backend/routes/auth.py`, `backend/routes/admin.py`

### Specifications
- **Algorithm**: Bcrypt salted hashing (`$2b$12$...` cost factor).
- **Security Guarantee**: One-way irreversible. Passwords can never be extracted from database dumps or SQL logs.
- **Verification Routine**:
  ```python
  import bcrypt

  # Password check on login
  is_valid = bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))
  ```

---

## 3. Database Schema Security Architecture

### A. `admins` Table
```sql
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL, -- AES-256 Encrypted ("BB_ENC:...")
    password VARCHAR(255) NOT NULL,         -- Bcrypt Hashed ("$2b$12$...")
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### B. `users` Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,        -- AES-256 Encrypted ("BB_ENC:...")
    email VARCHAR(255) UNIQUE NOT NULL,     -- AES-256 Encrypted ("BB_ENC:...")
    password_hash VARCHAR(255) NOT NULL,    -- Bcrypt Hashed ("$2b$12$...")
    phone VARCHAR(255) NULL,                -- AES-256 Encrypted ("BB_ENC:...")
    is_blocked BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Authentication & JWT Authorization Layer

### Architecture Location
- **Module**: `backend/middleware/auth.py`

### Multi-Tier Resilient JWT Decoder (`decode_jwt_token`)
- **Tier 1 (Primary)**: Decodes token using dynamic system secret (`Config.get_jwt_secret()`).
- **Tier 2 (Fallback Key Inspection)**: Handles multi-worker environment key drift across fallback keys.
- **Tier 3 (Expiry Protection)**: Rejects expired tokens automatically (`ExpiredSignatureError`).

### Route Protection Decorators
- **`@token_required`**: Ensures valid JWT bearer token and injects authenticated user context into request handlers.
- **`@admin_required`**: Validates admin role via JWT claims, `AdminModel` table query, or `UserModel.is_admin` flag.

---

## 5. Account Lockout & Brute-Force Rate Limiting

### Architecture Location
- **Modules**: `backend/models/user_attempt.py`, `backend/models/user_login_attempt.py`

### Mechanism
- Tracks consecutive failed authentication attempts by user ID.
- Automatically locks accounts for **15 minutes** upon exceeding failure thresholds:
  - **Login Failures**: Locked out on 5 consecutive invalid password attempts.
  - **OTP Rate Limit**: Locked out on excessive OTP request attempts.

---

## 6. Audit Trail & Administrative Logging

### Architecture Location
- **Modules**: `backend/utils/audit.py`, `backend/models/admin.py` (`AdminAuditLog`)

### Features
- Records administrative events (logins, status changes, user blocks, inventory stock modifications).
- Logs include: Admin identifier, action type, target module, detailed description, status, and IST timestamp.

---

## 7. Zero-`.env` Fallback Resilience

### Architecture Location
- **Module**: `backend/config.py`

### Specifications
- Centralized configuration system defaults to secure fallback keys for database connection strings, AES encryption digests, and JWT tokens if a `.env` file is missing.
- Allows immediate, zero-configuration local execution (`python3 -m backend.app`) while remaining fully compatible with environment variable overrides in production (e.g., Render, Railway, AWS).
