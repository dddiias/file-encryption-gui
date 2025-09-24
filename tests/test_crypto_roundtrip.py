import os, tempfile
from app.fs import encrypt_file, decrypt_file
from app.crypto.format import HEADER_LEN

PWD = "Pa$$w0rd"

def _mkbytes(n):
    return bytes((i * 31) % 256 for i in range(n))

def test_roundtrip_small():
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "a.bin")
        enc = src + ".encr"
        out = os.path.join(td, "a.out")
        open(src, "wb").write(_mkbytes(1024 * 64))
        encrypt_file(src, enc, PWD)
        decrypt_file(enc, out, PWD)
        assert open(src, "rb").read() == open(out, "rb").read()

def test_roundtrip_empty():
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "empty.bin")
        enc = src + ".encr"
        out = os.path.join(td, "empty.out")
        open(src, "wb").write(b"")
        encrypt_file(src, enc, PWD)
        decrypt_file(enc, out, PWD)
        assert open(src, "rb").read() == open(out, "rb").read()
        assert os.path.getsize(enc) == HEADER_LEN

def test_wrong_password_rejected():
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "b.bin")
        enc = src + ".encr"
        out = os.path.join(td, "b.out")
        open(src, "wb").write(_mkbytes(4096))
        encrypt_file(src, enc, PWD)
        try:
            decrypt_file(enc, out, "wrong")
            assert False, "Should fail on wrong password"
        except ValueError as e:
            assert "Wrong password" in str(e) or "Invalid file format" in str(e)
