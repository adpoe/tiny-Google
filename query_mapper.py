#! /usr/bin/python
"""
 Usage: test with -->
    cat books_inverted_index/part-00000 | python query_mapper.py | sort -k1,1 -k2,1
"""
import os
from sys import stdin
import ast



# Need some way to get the query words
# maybe append them as very first values in the input stream?
# or make them global variables somewhere we can read?


#keys = ['yours', 'you', 'yield', 'king', 'shield', 'young', 'yawned', 'yards', 'xfas']
#keys = []
dir_path = os.path.dirname(os.path.realpath(__file__))
keywords_file = dir_path + '/search_keywords.txt'
with open(keywords_file) as f:
    keywords = f.read()
    keys = ast.literal_eval(keywords)

# take each line in stdin from Hadoop streaming, one by one
for line in stdin:
    # in the last step, we separated by word, and a larger data structure containing
    # all necessary metadata we need for the query
    word_and_metadata = line.split('\t')

    # split the line into the word,
    # and the metadata about that word's occurrences in each book
    word = word_and_metadata[0]
    metadata = word_and_metadata[1]

    # only use the words that our user searched for
    if word not in keys:
        continue

    # de-structure our book data from previous step,
    # by splitting on the `;` char, which separates each book's metadta
    entries = metadata.split(';')

    # iterate through each entry in the book
    for entry in entries:
        # and create a data structure we can parse in the reducer,
        # and that contains the word, as well as its # occurrences, the book, and a list of indices
        # at which the word occurrence appeared on, within that book
        entry_data = entry.split(':')
        book = entry_data[0]
        occurrences = entry_data[1]
        listing = entry_data[2]

        print('%s\t%s:%s\t%s' % (word, occurrences, book, listing))
