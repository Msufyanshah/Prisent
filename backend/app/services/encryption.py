# backend/app/services/encryption.py
from cryptography.fernet import Fernet, InvalidToken
from app.config import settings

class DecryptionError(Exception):
    pass

def get_fernet() -> Fernet:
    key = settings.ENCRYPTION_KEY
    if not key:
        raise ValueError("ENCRYPTION_KEY not set in environment")
    return Fernet(key.encode() if isinstance(key, str) else key)

def encrypt_token(plain_token: str) -> str:
    """Encrypt a token for storage. Returns base64-encoded ciphertext."""
    f = get_fernet()
    return f.encrypt(plain_token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    """Decrypt a stored token. Raises DecryptionError if invalid/tampered."""
    f = get_fernet()
    try:
        return f.decrypt(encrypted_token.encode()).decode()
    except InvalidToken as e:
        raise DecryptionError("Token is invalid or has been tampered with") from e
