from typing import Callable, Optional

class XorShift32:
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF or 0xDEADBEEF

    def next_u32(self) -> int:
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state

    def next_bytes(self, n: int) -> bytes:
        out = bytearray()
        while len(out) < n:
            val = self.next_u32()
            out.extend(val.to_bytes(4, "little"))
        return bytes(out[:n])

def xor_stream_transform(
    read_chunk: Callable[[int], bytes],
    write_chunk: Callable[[bytes], None],
    total_bytes: int,
    prng: XorShift32,
    chunk_size: int = 1 << 20,
    progress_cb: Optional[Callable[[int, int], None]] = None,
    is_cancelled: Optional[Callable[[], bool]] = None,
) -> int:
    processed = 0
    while True:
        if is_cancelled and is_cancelled():
            break
        chunk = read_chunk(chunk_size)
        if not chunk:
            break
        ks = prng.next_bytes(len(chunk))
        out = bytes(a ^ b for a, b in zip(chunk, ks))
        write_chunk(out)
        processed += len(chunk)
        if progress_cb:
            progress_cb(processed, total_bytes)
    return processed
