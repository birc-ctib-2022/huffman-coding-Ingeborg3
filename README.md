# Huffman coding

[Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)
is an optimal way of encoding a string x = "..."[^1] in 
fewest bits, given that we wish each original character in the string
to appear at one unique position (i.e. we are not allowed to encode
substrings as single characters or represent them overlapping or other
tricks sometimes used in compression). This restriction is sometimes
important in algorithms where we need to be able to index into the
string efficiently, but that is a topic for another day (for example
a topic for GSA) and requries a few more tricks.

The simplest way to represent a string is with a fixed number of bits per
character. The [ASCII character set](https://en.wikipedia.org/wiki/ASCII),
for example uses 7 bits per character, although they are usually stored
in 8-bit bytes, originally using the extra bit as an error code.

If you do this, and your character set is `n` large, you need `log n` bits
per character, because that is how many bits you need to give each character
a unique number.

This is fine if all characters are equally likely to appear in a string,
but they aren't. There are special characters that you practically never see in
real life. And with [Unicode](https://en.wikipedia.org/wiki/Unicode) that
aims at being able to handle all the worlds languages and quite a few invented
languages as well, you only ever see a tiny sub-set of all characters.

It would be more efficient to use few bits for letters you see frequenty and
then pay for that by using more bits for rare characters. You still need to map
each character to a unique number, but they don't have to be represented in
the same number of bits.

Unicode itself only specifies the mapping from characters to numbers, but *encodings*
deal with how strings are stored, and an encoding such as
[`UTF-8`](https://en.wikipedia.org/wiki/UTF-8) puts the letters we are familiar
with in the West, such as the ASCII characters and letters in latin-based alphabets,
in one byte at the cost of using two or more for other characters.

Huffman encoding doesn't consern itself with bytes but individual bits and is a way
of mapping each character to a sequence of bits, such that the total number of bits
to represent is string is minimised.

The algorithm is described in the book (page 631), but in this exercise you get to
implement some of it yourself.

**Exercise:** In `src/huffman.py` impelement the `encoding(x: str) -> Tree` function
that builds a Huffman tree (basically a heap) from a string. 

**Exercise:** Implement the missing bit of the `build_encoding_table(...)` function. You
need to traverse the Huffman tree to extract the bit pattern that is matched to each letter.

**Exercise:** Implement the missing part of `decode(x: bits, enc: Encoding) -> str` that
recovers the original string from an encoding.





[^1]: A string in general terms, it can be any sequence over a finite set
of characters. But think strings as in English text or DNA or such. What you
think of as a string will work with Huffman coding.
