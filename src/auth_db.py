"""
SQLite Database Authentication & Cryptographic Security Module
Enterprise-Grade Security Architecture:
- PBKDF2-HMAC-SHA256 with 100,000 Key Derivation Iterations
- Cryptographically Secure Per-User 128-bit Random Salts (via secrets)
- Constant-Time Digest Verification (hmac.compare_digest) to eliminate timing attacks
- Seamless backward compatibility & in-place hash upgrades for legacy records
- Session Token Generation and Data Masking utilities for multi-tenant RBAC
"""

import os
import sqlite3
import hashlib
import hmac
import secrets
from datetime import datetime

DB_DIR = 'database'
DB_PATH = os.path.join(DB_DIR, 'ecommerce_bi.db')
PBKDF2_ITERATIONS = 100000
LEGACY_SALT = "ECommerceBI_Secure_2026"

def hash_password(password: str, salt: str = None) -> str:
    """
    Computes enterprise PBKDF2-HMAC-SHA256 hash with per-user cryptographic salt.
    Format: pbkdf2:sha256:<iterations>$<salt_hex>$<hash_hex>
    """
    if salt is None:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        PBKDF2_ITERATIONS
    )
    return f"pbkdf2:sha256:{PBKDF2_ITERATIONS}${salt}${key.hex()}"

def _hash_password(password: str) -> str:
    """Backward compatibility hook returning modern PBKDF2 hash."""
    return hash_password(password)

def verify_password(password: str, stored_hash: str) -> bool:
    """
    Validates a password against stored hash using constant-time comparison.
    Supports both modern PBKDF2 and legacy static-salt SHA-256 hashes.
    """
    if not stored_hash:
        return False

    if stored_hash.startswith("pbkdf2:sha256:"):
        try:
            parts = stored_hash.split('$')
            if len(parts) == 3:
                iter_str = parts[0].split(':')[-1]
                iterations = int(iter_str)
                salt = parts[1]
                expected_key_hex = parts[2]
                computed = hashlib.pbkdf2_hmac(
                    'sha256',
                    password.encode('utf-8'),
                    salt.encode('utf-8'),
                    iterations
                )
                return hmac.compare_digest(computed.hex(), expected_key_hex)
        except Exception:
            return False

    # Legacy static-salt fallback
    legacy_calc = hashlib.sha256((password + LEGACY_SALT).encode('utf-8')).hexdigest()
    return hmac.compare_digest(legacy_calc, stored_hash)

def generate_session_token() -> str:
    """Generates cryptographically random URL-safe session token."""
    return secrets.token_urlsafe(32)

def mask_sensitive_pii(text: str, mask_type: str = 'text') -> str:
    """
    Cryptographically safe data masking for lower-tier roles (Zero-Trust RBAC).
    """
    if not text or not isinstance(text, str):
        return text
    if mask_type == 'email' and '@' in text:
        user_part, domain = text.split('@', 1)
        masked_user = user_part[0] + '***' + user_part[-1] if len(user_part) > 2 else '***'
        return f"{masked_user}@{domain}"
    if len(text) > 4:
        return text[:2] + '•' * (len(text) - 4) + text[-2:]
    return '••••'

def init_db():
    """Initializes SQLite database, schema migrations, and seeds default accounts with PBKDF2."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_login TEXT,
        session_token TEXT,
        encryption_standard TEXT DEFAULT 'PBKDF2-HMAC-SHA256'
    )
    """)
    
    # Check if optional columns exist (schema migration safeguard)
    cursor.execute("PRAGMA table_info(users)")
    existing_cols = [col[1] for col in cursor.fetchall()]
    if 'last_login' not in existing_cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
        except sqlite3.OperationalError:
            pass
    if 'session_token' not in existing_cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN session_token TEXT")
        except sqlite3.OperationalError:
            pass
    if 'encryption_standard' not in existing_cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN encryption_standard TEXT DEFAULT 'PBKDF2-HMAC-SHA256'")
        except sqlite3.OperationalError:
            pass

    # Pre-seed / Upgrade default enterprise accounts
    default_users = [
        ("admin", "admin123", "Administrator", "Chief BI Architect"),
        ("analyst", "analyst123", "BI Analyst", "Senior Data Analyst"),
        ("manager", "manager123", "Business Manager", "Operations Director"),
        ("ops", "ops123", "Operations & Inventory Lead", "Supply Chain Director"),
        ("marketing", "marketing123", "Marketing & CRM Specialist", "Growth & Retention Lead")
    ]
    
    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for uname, pwd, role, fname in default_users:
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (uname,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute("""
            INSERT INTO users (username, password_hash, role, full_name, created_at, encryption_standard)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (uname, hash_password(pwd), role, fname, now_ts, "PBKDF2-HMAC-SHA256 (100k)"))
        else:
            # Upgrade existing legacy hash to PBKDF2 if needed
            uid, cur_hash = row
            if not cur_hash.startswith("pbkdf2:sha256:"):
                new_hash = hash_password(pwd)
                cursor.execute("""
                UPDATE users SET password_hash = ?, encryption_standard = 'PBKDF2-HMAC-SHA256 (100k)' WHERE id = ?
                """, (new_hash, uid))
            
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    """
    Authenticates username and password against SQLite database.
    Upgrades legacy password hashes in place upon successful authentication.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, username, password_hash, role, full_name, encryption_standard 
    FROM users WHERE username = ?
    """, (username,))
    user = cursor.fetchone()
    
    if user:
        uid, uname, stored_hash, role, fname, enc_std = user
        if verify_password(password, stored_hash):
            session_tok = generate_session_token()
            now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # If hash was legacy format, automatically re-hash with PBKDF2
            if not stored_hash.startswith("pbkdf2:sha256:"):
                upgraded_hash = hash_password(password)
                cursor.execute("""
                UPDATE users SET password_hash = ?, last_login = ?, session_token = ?, encryption_standard = 'PBKDF2-HMAC-SHA256 (100k)'
                WHERE id = ?
                """, (upgraded_hash, now_ts, session_tok, uid))
            else:
                cursor.execute("""
                UPDATE users SET last_login = ?, session_token = ? WHERE id = ?
                """, (now_ts, session_tok, uid))
                
            conn.commit()
            conn.close()
            
            return {
                'username': uname,
                'role': role,
                'full_name': fname,
                'session_token': session_tok,
                'encryption': 'PBKDF2-HMAC-SHA256 (100,000 iters)',
                'last_login': now_ts
            }
            
    conn.close()
    return None

def register_user(username, password, role="BI Analyst", full_name="Team Member"):
    """Registers a new user in the SQLite database with 100,000 iteration PBKDF2 encryption."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = False
    try:
        pwd_hash = hash_password(password)
        cursor.execute("""
        INSERT INTO users (username, password_hash, role, full_name, created_at, encryption_standard)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (username, pwd_hash, role, full_name, now_ts, "PBKDF2-HMAC-SHA256 (100k)"))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success

def list_users():
    """Returns list of registered users in the SQLite database (excluding password hashes)."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, username, role, full_name, created_at, IFNULL(encryption_standard, 'PBKDF2-HMAC-SHA256') 
    FROM users ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{
        "ID": r[0], 
        "Username": r[1], 
        "Role": r[2], 
        "Full_Name": r[3], 
        "Registered_At": r[4],
        "Encryption": r[5]
    } for r in rows]

if __name__ == '__main__':
    init_db()
    res = authenticate_user("admin", "admin123")
    print("Database initialized with PBKDF2-HMAC-SHA256.")
    print("Test login response:", res)
    print("Registered users count:", len(list_users()))
