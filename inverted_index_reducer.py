#! /usr/bin/python
"""
 Usage: test with -->
 cat books_preprocess/*.txt | python inverted_index_mapper.py | sort -k1,1 | python inverted_index_reducer.py
"""

from sys import stdin
import re

count_index = {}
occurrence_index = {}

for line in stdin:
    word, postings = line.split('\t')

    count_index.setdefault(word, {})
    occurrence_index.setdefault(word, {})

    for posting in postings.split(','):
        doc_id, count, line_num = posting.split(':')
        count = int(count)
        line_num = int(line_num)

        # handle count index
        count_index[word].setdefault(doc_id, 0)
        count_index[word][doc_id] += count

        # handle occurrence index
        occurrence_index[word].setdefault(doc_id, [])
        occurrence_index[word][doc_id].append(line_num)

for word in count_index:
    postings_list = ["%s:%d:%s" % (doc_id, count_index[word][doc_id], str(occurrence_index[word][doc_id]))
                     for doc_id in count_index[word]]

    postings = ','.join(postings_list)
    print('%s\t%s' % (word, postings))