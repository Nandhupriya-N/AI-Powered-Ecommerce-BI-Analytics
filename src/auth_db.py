"""
SQLite Database Authentication & Cryptographic Security Module
Enterprise-Grade Security Architecture:
- PBKDF2-HMAC-SHA256 with 100,000 Key Derivation Iterations
- Cryptographically Secure Per-User 128-bit Random Salts (via secrets)
- Constant-Time Digest Verification (hmac.compare_digest) to eliminate timing attacks
- Seamless backward compatibility & in-place hash upgrades for legacy records
- Session Token Generation, Audit Logging (Login/Logout), and RBAC Custom Module Provisioning
"""

import os
import sqlite3
import hashlib
import hmac
import secrets
import json
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

def log_activity(username: str, full_name: str, role: str, action: str, details: str = ""):
    """Records an immutable security audit event into the SQLite audit_logs table."""
    try:
        os.makedirs(DB_DIR, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO audit_logs (username, full_name, role, action, timestamp, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (username, full_name, role, action.upper(), now_ts, details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Audit log record failed: {e}")

def get_audit_logs(limit: int = 150):
    """Retrieves recent login, logout, and user administrative activity logs."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, username, full_name, role, action, timestamp, IFNULL(details, '')
    FROM audit_logs
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{
        "ID": r[0],
        "Timestamp": r[5],
        "Username": r[1],
        "Full_Name": r[2],
        "Role": r[3],
        "Action": r[4],
        "Details": r[6]
    } for r in rows]

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
        encryption_standard TEXT DEFAULT 'PBKDF2-HMAC-SHA256',
        custom_modules TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        action TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        details TEXT
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
    if 'custom_modules' not in existing_cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN custom_modules TEXT")
        except sqlite3.OperationalError:
            pass

    # Ensure 'ops' user is purged from database as requested
    cursor.execute("DELETE FROM users WHERE username = 'ops'")

    # Pre-seed / Upgrade default enterprise accounts (excluding ops)
    default_users = [
        ("admin", "admin123", "Administrator", "Chief BI Architect"),
        ("analyst", "analyst123", "BI Analyst", "Senior Data Analyst"),
        ("manager", "manager123", "Business Manager", "Operations Director"),
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
    Logs successful login into the audit_logs table.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, username, password_hash, role, full_name, encryption_standard, custom_modules 
    FROM users WHERE username = ?
    """, (username,))
    user = cursor.fetchone()
    
    if user:
        uid, uname, stored_hash, role, fname, enc_std, raw_custom_mods = user
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

            # Record Login event in security audit trail
            log_activity(uname, fname, role, 'LOGIN', 'Authenticated via PBKDF2-HMAC-SHA256')
            
            custom_mods_list = None
            if raw_custom_mods:
                try:
                    custom_mods_list = json.loads(raw_custom_mods)
                except Exception:
                    custom_mods_list = None

            return {
                'username': uname,
                'role': role,
                'full_name': fname,
                'session_token': session_tok,
                'encryption': 'PBKDF2-HMAC-SHA256 (100,000 iters)',
                'last_login': now_ts,
                'custom_modules': custom_mods_list
            }
            
    conn.close()
    return None

def create_new_user(username, password, role="BI Analyst", full_name="Team Member", custom_modules=None, performed_by="admin") -> tuple[bool, str]:
    """
    Registers a new user in the SQLite database with 100,000 iteration PBKDF2 encryption
    and custom module provisions. Logs USER_CREATED event in audit log.
    """
    init_db()
    uname = username.strip().lower()
    if not uname or len(uname) < 3:
        return False, "Username must be at least 3 characters."
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters."
    if uname == 'ops':
        return False, "'ops' username is deprecated and cannot be created."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        pwd_hash = hash_password(password)
        custom_mod_json = json.dumps(custom_modules) if custom_modules else None
        cursor.execute("""
        INSERT INTO users (username, password_hash, role, full_name, created_at, encryption_standard, custom_modules)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (uname, pwd_hash, role, full_name.strip(), now_ts, "PBKDF2-HMAC-SHA256 (100k)", custom_mod_json))
        conn.commit()
        conn.close()

        mod_count_desc = f"{len(custom_modules)} modules" if custom_modules else f"Default for {role}"
        log_activity(performed_by, performed_by, "Administrator", "USER_CREATED", f"Created user @{uname} ({full_name.strip()}, Role: {role}, Provisioned: {mod_count_desc})")
        return True, f"User @{uname} created successfully with {mod_count_desc}."
    except sqlite3.IntegrityError:
        conn.close()
        return False, f"Username @{uname} already exists."
    except Exception as e:
        conn.close()
        return False, f"Database error: {str(e)}"

def register_user(username, password, role="BI Analyst", full_name="Team Member", custom_modules=None, performed_by="admin") -> bool:
    """Backward-compatible boolean wrapper for user creation."""
    success, _ = create_new_user(username, password, role, full_name, custom_modules, performed_by)
    return success

def delete_user(username: str, performed_by: str = "admin") -> tuple[bool, str]:
    """Deletes a user from the SQLite database with protection for primary administrator."""
    uname = username.strip().lower()
    if uname == 'admin':
        return False, "Cannot delete primary administrator account (@admin)."
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT full_name, role FROM users WHERE username = ?", (uname,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, f"User @{uname} not found."
        fname, role = row
        cursor.execute("DELETE FROM users WHERE username = ?", (uname,))
        conn.commit()
        conn.close()
        log_activity(performed_by, performed_by, "Administrator", "USER_DELETED", f"Deleted user @{uname} ({fname}, Role: {role})")
        return True, f"User @{uname} successfully removed."
    except Exception as e:
        conn.close()
        return False, f"Error deleting user: {str(e)}"

def update_user_modules(username: str, custom_modules: list, performed_by: str = "admin") -> tuple[bool, str]:
    """Updates custom module permissions for a user."""
    uname = username.strip().lower()
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        mod_json = json.dumps(custom_modules) if custom_modules is not None else None
        cursor.execute("UPDATE users SET custom_modules = ? WHERE username = ?", (mod_json, uname))
        conn.commit()
        conn.close()
        mod_desc = f"{len(custom_modules)} custom modules" if custom_modules else "Role Default modules"
        log_activity(performed_by, performed_by, "Administrator", "PERMISSIONS_UPDATED", f"Updated modules for @{uname} to {mod_desc}")
        return True, f"Permissions for @{uname} updated successfully to {mod_desc}."
    except Exception as e:
        conn.close()
        return False, f"Failed to update permissions: {str(e)}"

def list_users():
    """Returns list of registered users in the SQLite database (excluding password hashes)."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, username, role, full_name, created_at, IFNULL(encryption_standard, 'PBKDF2-HMAC-SHA256'), last_login, custom_modules 
    FROM users ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    result = []
    for r in rows:
        c_mods = None
        if r[7]:
            try:
                c_mods = json.loads(r[7])
            except Exception:
                c_mods = None
        result.append({
            "ID": r[0], 
            "Username": r[1], 
            "Role": r[2], 
            "Full_Name": r[3], 
            "Registered_At": r[4],
            "Encryption": r[5],
            "Last_Login": r[6] or "Never",
            "Custom_Modules": c_mods
        })
    return result

if __name__ == '__main__':
    init_db()
    res = authenticate_user("admin", "admin123")
    print("Database initialized with PBKDF2-HMAC-SHA256.")
    print("Test login response:", res)
    print("Registered users count:", len(list_users()))
    print("Audit logs count:", len(get_audit_logs()))
