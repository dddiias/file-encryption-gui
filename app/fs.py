import os
from typing import Callable, Optional
from .crypto.algo import XorShift32, xor_stream_transform
from .crypto.format import write_header, read_header, HEADER_LEN

DEFAULT_CHUNK = 1 << 20

def encrypt_file(
    src_path: str,
    dst_path: str,
    password: str,
    chunk_size: int = DEFAULT_CHUNK,
    progress_cb: Optional[Callable[[int, int], None]] = None,
    is_cancelled: Optional[Callable[[], bool]] = None,
) -> None:
    total = os.path.getsize(src_path)
    with open(src_path, "rb") as fin, open(dst_path, "wb") as fout:
        seed = write_header(fout, password)
        prng = XorShift32(seed)
        xor_stream_transform(
            fin.read, fout.write, total, prng,
            chunk_size=chunk_size,
            progress_cb=progress_cb,
            is_cancelled=is_cancelled,
        )

def decrypt_file(
    src_path: str,
    dst_path: str,
    password: str,
    chunk_size: int = DEFAULT_CHUNK,
    progress_cb: Optional[Callable[[int, int], None]] = None,
    is_cancelled: Optional[Callable[[], bool]] = None,
) -> None:
    total = max(0, os.path.getsize(src_path) - HEADER_LEN)
    with open(src_path, "rb") as fin, open(dst_path, "wb") as fout:
        seed = read_header(fin, password)
        prng = XorShift32(seed)
        xor_stream_transform(
            fin.read, fout.write, total, prng,
            chunk_size=chunk_size,
            progress_cb=progress_cb,
            is_cancelled=is_cancelled,
        )
