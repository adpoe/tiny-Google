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
    metadata_and_line = line.split('\\t')  # double tab because sed places an escaped tab, \\t
                                           # when we pre-process input

    # if we have a blank line, skip to next
    if len(metadata_and_line) < 2:
        continue

    # these need to be split on just one '\t', because of the output from nl
    line_num_and_fname = metadata_and_line[0].split('\t')

    # assign document id and text, from what we've split
    line_num = int(line_num_and_fname[0])
    book_name = line_num_and_fname[1]
    text = metadata_and_line[1]

    # can use this print to check that splits are working
    # print(split)

    # use regex to split the line into words
    # picking regex in case there is a delimiter like '-', or '--', or ';',
    # or other besides just ' ', whitespace. This handles all whitespace.
    words = re.findall(r'\w+', text.strip())

    # make sure we are looking at same document before setting previous line's text
    # map each word and the doc id
    for word in words:
        # standardize words to lowercase
        word = word.lower()
        # then output, passing them to reducer
        print("%s\t%s:1:%s" % (word, book_name, line_num))
