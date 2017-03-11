#! /usr/bin/python
"""
Inverted Index Mapper
    - Input:  Preprocessed Book.txt file. Must have doc_id\t as prefix for every line
    - Test with;
        * cat books_preprocess/AdventuresOfHuckleberryFinnByMarkTwain.txt | python inverted_index_mapper.py | sort -k1,1
"""

from sys import stdin
import re


for line in stdin:
    # clean \r\n from end of lines (Mac)
    line = line.strip()

    # split each line by on tabs, to get the document id, and then actual text
    split = line.split('\\t')  # double tab because sed places an escaped tab, \\t
                               # when we pre-process input

    # if we have a blank line, skip to next
    if len(split) < 2:
        continue

    # assign document id and text, from what we've split
    doc_id = split[0]
    text = split[1]

    # can use this print to check that split are working
    # print(split)

    # use regex to split the line into words
    # picking regex in case there is a delimiter like '-', or '--', or ';',
    # or other besides just ' ', whitespace. This handles all whitespace.
    words = re.findall(r'\w+', text.strip())

    # map each word and the doc id
    for word in words:
        print("%s\t%s:1" % (word.lower(), doc_id))