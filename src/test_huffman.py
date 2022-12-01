"""Test Huffman coding"""

from huffman import Encoding


def test_minimal() -> None:
    """You will want to test more than this..."""
    x = "aabacabaaa"
    enc = Encoding(x)
    assert x == enc.decode(enc.encode(x))
