# auth.py
import bcrypt
from db import get_user_by_username, create_user

def hash_password(password: str) -> str:
    """Return bcrypt hash of the given password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a plaintext password against the stored bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def register_user(username: str, password: str):
    if get_user_by_username(username):
        raise ValueError("Username already exists")
    pw_hash = hash_password(password)
    return create_user(username, pw_hash)
