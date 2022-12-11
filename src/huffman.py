"""
Huffman coding.

Code for constructing an encoding from a string and for encoding
and decoding strings given an encoding.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Optional, Iterator
from collections import Counter
import heapq as hq

# We will use strings of 0 and 1 to represent bits as actually
# working with bits is a little more involved and beyond the
# scope of this class. I might show you how in the programming
# club some day.
bits = str
# We don't have separate letters and strings in Python, so we
# just pretend that we do
letters = str

# MixIn for comparing nodes


class CountCmp:
    """
    The comparison operator for the two types of nodes.

    This class doesn't do anything by itself, but if we
    inherit it as a mixin we get the comparsion we need
    in both tree classes.
    """

    count: int  # We expect this one

    def __lt__(self, other: CountCmp) -> bool:
        """Test if self has more counts than other."""
        return self.count < other.count


@dataclass
class Leaf(CountCmp):
    """A leaf of a Huffman tree contains a letter."""

    letter: letters  # The letter we are encoding
    count: int       # How often have we seen the letter.


@dataclass
class Node(CountCmp):
    """An inner node contains references to a left and right tree."""

    count: int   # How often have we seen a letter in this subtree
    left: Tree
    right: Tree


Tree = Union[Leaf, Node] 



def encoding(x: str) -> Tree: # build_huffmann_tree().
    """Create Huffman tree for `x`.
    >>> x='aabacabaaa'
    >>> encoding(x)
    Node(count=10, left=Node(count=3, left=Leaf(letter='c', count=1),\
 right=Leaf(letter='b', count=2)), right=Leaf(letter='a', count=7))
    """
    # Make a heap out of all the leaves, i.e. counts of the letters.
    heap: list[Tree] = [Leaf(a, count) for a, count in Counter(x).items()]
    # heap = [Leaf(letter='a', count=3), Leaf(letter='b', count=1), 
    # Leaf(letter='c', count=1)]
    hq.heapify(heap) # the list representation of the heap is 
    # 'heapified' so that it meets the min heap invariant. The values
    # of the heap are Leafs to begin with and later on Nodes. 
    # The counts for the letters are stored inside the nodes.  
    # heap = [Leaf(letter='c', count=1), Leaf(letter='b', count=1), 
    # Leaf(letter='a', count=3)]

    while len(heap) > 1: # when heap only contains one Node, the loop 
        # body of the while loop will no longer be executed, and the 
        # node of the heap will be returned. This node is the final 
        # HuffmanTree.

        # Get the first two trees from the heap,
        # merge them into one new Node with a count that
        # is the sum of the two trees, and with the two
        # trees as subtrees. Push that back onto the heap.
        # Remember that heap.pop() and heap.append() are
        # list operations, but you need to use the hq.heappop()
        # or hq.heappush() functions.
        
        # hq.heappop() corresponds to delete_min(). Here, the value it
        # returns is a Leaf or a Node. 
        left = hq.heappop(heap)
        right = hq.heappop(heap)
        count = left.count + right.count
        hq.heappush(heap, Node(count, left, right))

    return hq.heappop(heap) # deletes the root node and return its 
    # value. The values of the binary heap created using heapq.heapify
    # are Huffman Trees. 

def build_encoding_table(tree: Tree,
                         bits: list[bits, ...] = [], # list of single
                         # bits as strings in book.
                         table: Optional[dict[letters, bits]] = None, 
                         # called table in book. dictionary w. string-
                         # letters as keys and string-bits as values.
                         ) -> dict[letters, bits]:
    """Traverse the tree to get the mapping for letters.
    >>> x = 'aabacabaaa'
    >>> tree = encoding(x)
    >>> build_encoding_table(tree)
    {'c': '00', 'b': '01', 'a': '1'}
    """
    # The bits argument is intended as an accumulator of bits
    # i.e. strings "0" or "1". If you are in a leaf, you can
    # "".join(bits) to get the bit pattern. If not, you can
    # recursively go down the tree to build the bit-patterns
    # for each sub-tree. When you go left, add a 0 to bits and
    # when you go right, add a 1. This isn't the most efficient
    # solution, but it gets the job done, and we don't expect
    # large trees in an application like this.
    table = table if table is not None else {} # 'table' in 'if table' 
    # evaluates to False if table = None and if table = {}.
    if isinstance(tree, Leaf): # isinstance() returns True if the 
        # object given as the first argument is of the type given by
        # the second argument. 
        # isinstance(tree, Leaf) returns True if the tree is an object
        # of the type Leaf.
        table[tree.letter] = ''.join(bits)
        return table
    else:
        # go to the left
        bits.append('0')
        build_encoding_table(tree.left, bits, table)
        # go to parent
        bits.pop()
        # go to the right
        bits.append('1')
        build_encoding_table(tree.right, bits, table)
        # go to parent
        bits.pop()
        return table


class BitIterator:
    """
    Iterate through bits.

    This is a wrapper that makes it slightly easier to iterate
    over a sequence of bits in our application. Python's iterators
    do not have a method for checking if you have more bits, but
    relies on the StopIteration exception. Using that is the
    Pythonic way of doing it, but here I think it is easier to
    ask for the next element and be told whether there is one
    or not...
    """

    bit_itr: Iterator[bits]

    def __init__(self, x: bits): 
        """Set up the iterator."""
        self.bit_itr = iter(x)

    def next(self) -> bits | None:
        """
        Get the next bit.

        If there are no more bits, you get None.
        """
        try:
            return next(self.bits)
        except StopIteration:
            return


# hvilken type object er x, siden det er nødvendigt med iter(x)?
# enc er et object af typen Encoding. enc.tree giver et Huffmann tree
# for en string. enc.table giver en dictionary med letters som keys og
# bit-strings som values.
def decode(x: bits, enc: Encoding) -> str:
    """Decode the bit pattern x according to enc.
    >>> decode('1101100101111', Encoding('aabacabaaa'))
    'aabacabaaa'
    """
    bits = iter(x)  # Makes it easier to run thought the bits
    node = enc.tree  # We start in the root
    decoding: list[str] = [] # list with letters. 

    # When we have no more bits and ask for the next, we get
    # a StopIteration. We will catch that and deal with it
    # below
    try:
        while True:  # we break when there are no more bits
            # Handle the current node.
            # If it is a leaf, you want to add its letter to
            # decoding, and after that you should go back to
            # the root.
            # If it is an inner node, you need to get the next
            # bit, you can do that with `b = next(bits)`, and
            # then you move the node to the left or right child
            # based on the bit.

            # b = next(bits) skal også bruges for at få den første bit.
            b = next(bits)
            if b == '0':
                node = node.left
            if b == '1': 
                node = node.right
            if isinstance(node, Leaf):
                decoding.append(node.letter)
                node = enc.tree
    except StopIteration: # How come StopIteration exception, when this
        # already handled in the next() method?
        # When we asked for a bit that wasn't there, we end
        # up here. We need to wrap up. We should only ever
        # end here when we are in the root, so we assert that
        assert enc.tree is node
    # and if that is fine, we can return the decoding
    return "".join(decoding)

class Encoding:
    """Class used for Huffman encoding and decoding."""

    tree: Tree  # The Huffman tree for the encoding.
    table: dict[letters, bits]  # Maps each letter to a bit-pattern 

    def __init__(self, x: str):
        """Create the encoding for `x`."""
        self.tree = encoding(x) # build_huffmann_tree()
        self.table = build_encoding_table(self.tree) 

    def encode(self, x: str) -> bits:
        """Encode the string x according to the encoding."""
        return "".join(self.table[letter] for letter in x)

    def decode(self, x: bits) -> str:
        """Decode x according to this encoding."""
        return decode(x, self)