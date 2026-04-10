"""Short-code helpers: Base62 encoding of integer primary keys."""

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_encode(n: int) -> str:
    """Encode a non-negative integer as a Base62 string (deterministic, URL-safe)."""
    if n < 0:
        raise ValueError("base62_encode expects a non-negative integer")
    if n == 0:
        return BASE62_ALPHABET[0]
    digits: list[str] = []
    value = n
    while value:
        value, rem = divmod(value, 62)
        digits.append(BASE62_ALPHABET[rem])
    return "".join(reversed(digits))


def base62_decode(s: str) -> int:
    """Decode a Base62 string back to an integer (inverse of base62_encode)."""
    if not s:
        raise ValueError("empty string")
    n = 0
    for ch in s:
        idx = BASE62_ALPHABET.find(ch)
        if idx < 0:
            raise ValueError(f"invalid base62 character: {ch!r}")
        n = n * 62 + idx
    return n
