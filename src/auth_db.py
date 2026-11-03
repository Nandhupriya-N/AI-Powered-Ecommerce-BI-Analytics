"""
SQLite Database Authentication Module
Handles persistent user credentials, hashed passwords, and role management.
"""

import os
import sqlite3
import hashlib
from datetime import datetime

DB_DIR = 'database'
DB_PATH = os.path.join(DB_DIR, 'ecommerce_bi.db')

def _hash_password(password: str) -> str:
    """Returns SHA-256 hash of password with fixed salt."""
    salt = "ECommerceBI_Secure_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def init_db():
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
        created_at TEXT NOT NULL
    )
    """)
    
    # Pre-seed default accounts
    default_users = [
        ("admin", "admin123", "Administrator", "Chief BI Architect"),
        ("analyst", "analyst123", "BI Analyst", "Senior Data Analyst"),
        ("manager", "manager123", "Business Manager", "Operations Director"),
        ("ops", "ops123", "Operations & Inventory Lead", "Supply Chain Director"),
        ("marketing", "marketing123", "Marketing & CRM Specialist", "Growth & Retention Lead")
    ]
    
    for uname, pwd, role, fname in default_users:
        cursor.execute("SELECT id FROM users WHERE username = ?", (uname,))
        if cursor.fetchone() is None:
            cursor.execute("""
            INSERT INTO users (username, password_hash, role, full_name, created_at)
            VALUES (?, ?, ?, ?, ?)
            """, (uname, _hash_password(pwd), role, fname, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    """Verifies username and password against database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    pwd_hash = _hash_password(password)
    cursor.execute("SELECT username, role, full_name FROM users WHERE username = ? AND password_hash = ?", (username, pwd_hash))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'username': user[0],
            'role': user[1],
            'full_name': user[2]
        }
    return None

def register_user(username, password, role="BI Analyst", full_name="Team Member"):
    """Registers a new user in the SQLite database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO users (username, password_hash, role, full_name, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (username, _hash_password(password), role, full_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
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
    cursor.execute("SELECT id, username, role, full_name, created_at FROM users ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [{"ID": r[0], "Username": r[1], "Role": r[2], "Full_Name": r[3], "Registered_At": r[4]} for r in rows]

if __name__ == '__main__':
    init_db()
    res = authenticate_user("admin", "admin123")
    print("Database initialized. Test login:", res)
    print("Registered Users:", list_users())
