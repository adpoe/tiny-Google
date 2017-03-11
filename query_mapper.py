#! /usr/bin/python
"""
 Usage: test with -->
    cat books_inverted_index/part-00000 | python query_mapper.py | sort -k1,1 -k2,1
"""

from sys import stdin

for line in stdin:
    word_and_metadata = line.split('\t')
    #print(str(word_and_metadata) + '\n')

    word = word_and_metadata[0]
    metadata = word_and_metadata[1]

    entries = metadata.split(';')

    for entry in entries:
        entry_data = entry.split(':')
        book = entry_data[0]
        occurrences = entry_data[1]
        listing = entry_data[2]

        print('%s\t%s:%s\t%s' % (word, occurrences, book, listing))