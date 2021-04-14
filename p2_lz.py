import os
import numpy as np
import math

INPUT_FILE = "genome.txt"


coded_message = []
coded_bin = ""

prefix = ""
prefixes = {"" : 0}


with open(INPUT_FILE, 'r') as f:

    # The whole point of this trickery is to detect
    # EOF one char ahead. This way we can tell when
    # we're processing the last character of the
    # input file

    c = f.read(1)
    eof = c == ''
    next_char = f.read(1)

    while True:
        if not eof and prefix + c in prefixes:
            prefix = prefix + c
        else:
            # coded_message.append( [prefixes[prefix], c] )

            # FIXME one must optimize this
            l = math.ceil(math.log2(len(prefixes)))
            if l == 0:
                l = 1

            coded_bin += f"{np.binary_repr(prefixes[prefix],l)}{ord(c):08b}"

            prefixes[prefix + c] = len(prefixes)
            prefix = ""

        if next_char != '':
            c = next_char
            next_char = f.read(1)
            eof = next_char == ''
        else:
            break

print(os.path.getsize(INPUT_FILE))

# Test : from 0/1 string to np array
as_bin = np.frombuffer(np.array(map(int, coded_bin)), np.uint8)
print(as_bin)
print(np.unpackbits(as_bin)[0:len(coded_bin)])

print(len(coded_bin) // 8)
# print(coded_bin)

ndx = 0
decoded = ""
prefixes = {0: ""}
while ndx < len(coded_bin):
    l = math.ceil(math.log2(len(prefixes)))
    if l == 0:
        l = 1
    prefix_code = int(coded_bin[ndx:ndx+l], 2)

    #print(f"ndx:{ndx}, l:{l}, len pfx:{len(prefixes)}, pfx code:{prefix_code}")
    c = chr(int(coded_bin[ndx+l:ndx+l+8], 2))
    # c = coded_bin[ndx+l:ndx+l+1]

    decoded += prefixes[prefix_code] + c
    #print(l,prefix_code,c,decoded)

    prefixes[len(prefixes)] = prefixes[prefix_code] + c
    ndx = ndx+l+8

# decoded = ""
# prefixes = {0: ""}
# for prefix_code, c in coded_message:
#     prefixes[len(prefixes)] = prefixes[prefix_code] + c
#     decoded += prefixes[prefix_code] + c

#print(decoded)

with open(INPUT_FILE, 'r') as f:
    assert decoded == f.read()


"""
**********************************************************************
Question 11 :
**********************************************************************
11. Famous data compression algorithms combine the LZ77 algorithm and the Huffman algorithm.
Explain how these algorithms can be combined and discuss the interest of the possible combinations.


A/ Using LZ77 first and Huffman second.

https://stackoverflow.com/questions/55547113/why-to-combine-huffman-and-lz77
https://cstheory.stackexchange.com/questions/7653/why-does-huffman-coding-eliminate-entropy-that-lempel-ziv-doesnt

If one assume there is a set of initial symbols, letters for example, then it is possible
to combine those in bigger symbols if we see repetitions, words for example. Doing, so
we can build a bigger set of symbols $S$ but, in exchange, represent the initial data with
a shorter sequence of symbols $R$. That’s what LZ77 does. It builds a better symbol set,
capturing repetitions. Of course, this makes sense only if we assume that repetitions
are occuring often enough.

So, once the better set of symbols and the associated sequence of symbols are built,
one can use Huffman to compress them. Huffman will build an optimal code book for
representing the symbols given by LZ77.

In practice, the symbols produced by LZ77 are tuples (jump, length, symbol).
Given how many bits we allow to represent each element,  these symbols may
be bigger than what they actually represent. So even if repetitions are caught
by LZ77, we see that the triplets

Given Huffman is parameterless algorithm and leads to an optimal coding, the only variable left is the sliding window
size of LZ77. The bigger the sliding window, the more repetitions, the shorter the sequence $R$, but,
the deeper the Huffman tree. So a balance must be found.


B/ Using Huffman first and  LZ77 second.





---- quest 11, remaining stuff

1/ run LZ77 directly, then compress each tuple the output with Huffman

"famous" algorithm like

MS-XCA : LZ77, then compress tuple with Huffman
DEFLATE : LZSS (not LZ77!) + canonical Huffman

https://stackoverflow.com/questions/55547113/why-to-combine-huffman-and-lz77

LZ77 est sliding windows mais quid huffman ? => use blocks : cut original file sin blocks



**********************************************************************
Question 12 : what does "the best" mean ? The fastest to compress ? decompress ? The one that produces shortest files ?
**********************************************************************

"""
