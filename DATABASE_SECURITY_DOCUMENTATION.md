# Database Security, Hashing & Encryption Documentation

This document provides technical documentation of the data security, password hashing, and column encryption architecture implemented for database tables (specifically `users`, `admins`, and `delivery_addresses`) in **Neon DB (PostgreSQL)** for the SSJewellery platform.

---

## 1. Hashing vs. Encryption Architecture Strategy

The platform segregates security approaches based on data sensitivity and operational requirements:

| Security Domain | Target Fields | Algorithm / Mechanism | Reversibility | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **User & Admin Passwords** | `users.password_hash`, `admins.password` | **Bcrypt** (`$2b$12$...`) | **Irreversible** (One-Way Hash) | Secure login verification via `bcrypt.checkpw()` |
| **Customer PII** | `users.full_name`, `users.email`, `users.phone` | **AES-256-CBC** (`BB_ENC:...`) | **Reversible** (Two-Way Encryption) | Protecting user data at rest in Neon DB while permitting UI decryption |
| **Address Information** | `delivery_addresses` columns | **AES-256-CBC** (`EncryptedString`) | **Reversible** (Two-Way Encryption) | Safeguard shipping locations at rest |
| **Admin Identity** | `admins.username` (Optional obfuscation) | **SHA-256** or **AES-256** | **One-Way / Two-Way** | Deterministic lookup / obfuscated administrative storage |

---

## 2. Technical Implementation Specifications

### A. One-Way Password Hashing (Bcrypt)

1. **Algorithm**: Blowfish Cipher (Bcrypt) with standard salt generation.
2. **Format Identifier**: Strings prefixed with `$2b$12$` or `$2a$12$`.
3. **Key Features**:
   - Includes salt automatically in the hash payload to defend against rainbow table attacks.
   - Irreversible by design (plaintext password cannot be extracted from database dumps).
4. **Verification Code Path**:
   ```python
   # Verifying password during authentication
   is_valid = bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))
   ```

---

### B. Two-Way Column Encryption (`EncryptedString` via AES-256-CBC)

1. **Implementation**: Custom SQLAlchemy `TypeDecorator` (`EncryptedString`) located in `backend/utils/security.py`.
2. **Cipher Specification**: **AES-256-CBC** with PKCS7 padding.
3. **Key Derivation**: 256-bit key generated from the server's `ENCRYPTION_KEY` environment variable (falling back to SHA-256 key digest).
4. **IV Derivation**: 16-byte synthetic Initialization Vector derived deterministically from plaintext SHA-256 digest (`get_deterministic_iv`).
5. **Database Storage Format**:
   ```text
   BB_ENC:<Base64Encoded(16-byte IV + AES Ciphertext)>
   ```
6. **Automated ORM Lifecycle**:
   - **On Database Insert/Update**: `EncryptedString.process_bind_param()` automatically encrypts plaintext string and prepends `BB_ENC:`.
   - **On Database Query**: `EncryptedString.process_result_value()` automatically detects `BB_ENC:`, decrypts payload, and returns unencrypted text in application memory.

---

## 3. Database Schema Mapping

### `users` Table Security Mapping

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,    -- AES-256 Encrypted (BB_ENC:...)
    email VARCHAR(255) UNIQUE NOT NULL, -- AES-256 Encrypted (BB_ENC:...)
    password_hash VARCHAR(255) NOT NULL, -- Bcrypt Hashed ($2b$12$...)
    phone VARCHAR(255) NULL,            -- AES-256 Encrypted (BB_ENC:...)
    is_blocked BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `admins` Table Security Mapping

```sql
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL, -- Plaintext, AES Encrypted, or SHA-256 Hashed
    password VARCHAR(255) NOT NULL          -- Bcrypt Hashed ($2b$12$...)
);
```

---

## 4. Key Security Guidelines

1. **Passwords**: Must always be stored using salted one-way hashing (`Bcrypt`). Never attempt to store passwords using reversible AES encryption.
2. **Customer Personal Data**: Stored encrypted at rest (`BB_ENC:...`) so that direct SQL exports of Neon DB contain zero plain text PII.
3. **Environment Security**: The secret encryption key (`ENCRYPTION_KEY`) must be maintained securely in server environment configurations.
