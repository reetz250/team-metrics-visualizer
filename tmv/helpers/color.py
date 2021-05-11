from typing import Tuple


def hex_to_rgb(s: str) -> Tuple[int, int, int]:
    """Converts hex color str to R, G, B values
    >>> hex_to_rgb('#ff00aa')
    (255, 0, 170)
    """
    s = s.lstrip("#")

    if len(s) == 6:  # e.g. ff00aa
        return tuple(rgb_long_hex(s))
    elif len(s) == 3:  # e.g. f0a -> ff00aa
        return tuple(rgb_short_hex(s))

    raise ValueError("Should be in #xxxxxx or #xxx format")


def rgb_long_hex(s):
    for i in range(0, len(s), 2):
        yield int(s[i : i + 2], 16)


def rgb_short_hex(s):
    for i in s:
        yield int(i * 2, 16)
