import hmac
import hashlib
from typing import BinaryIO
from .kdf import derive_key_material, make_salt

MAGIC = b"ENCR1"
SALT_LEN = 16
HDR_MAC_LEN = 4
HEADER_LEN = len(MAGIC) + SALT_LEN + HDR_MAC_LEN

def _hdr_mac(key_material: bytes, magic: bytes, salt: bytes) -> bytes:
    mac = hmac.new(key_material, magic + salt, hashlib.sha256).digest()
    return mac[:HDR_MAC_LEN]

def write_header(fout: BinaryIO, password: str) -> int:
    salt = make_salt(SALT_LEN)
    key_material = derive_key_material(password, salt)
    mac4 = _hdr_mac(key_material, MAGIC, salt)
    fout.write(MAGIC)
    fout.write(salt)
    fout.write(mac4)
    seed = int.from_bytes(key_material[:4], "little")
    return seed

def read_header(fin: BinaryIO, password: str) -> int:
    magic = fin.read(len(MAGIC))
    if magic != MAGIC:
        raise ValueError("Invalid file format: bad MAGIC")
    salt = fin.read(SALT_LEN)
    if len(salt) != SALT_LEN:
        raise ValueError("Invalid file format: short SALT")
    mac4 = fin.read(HDR_MAC_LEN)
    if len(mac4) != HDR_MAC_LEN:
        raise ValueError("Invalid file format: short HDR_MAC")

    key_material = derive_key_material(password, salt)
    expected = _hdr_mac(key_material, MAGIC, salt)
    if mac4 != expected:
        raise ValueError("Wrong password or corrupted header")

    seed = int.from_bytes(key_material[:4], "little")
    return seed
