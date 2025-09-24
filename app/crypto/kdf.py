import hashlib
import os

PBKDF2_ITERATIONS = 100_000
DK_LEN = 32

def derive_key_material(password: str, salt: bytes) -> bytes:
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be non-empty string")
    if not isinstance(salt, (bytes, bytearray)) or len(salt) < 8:
        raise ValueError("Salt must be bytes (>=8 bytes)")
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=DK_LEN,
    )

def make_salt(length: int = 16) -> bytes:
    return os.urandom(length)
