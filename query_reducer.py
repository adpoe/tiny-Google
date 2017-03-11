#! /usr/bin/python
"""
 Usage: test with -->
    cat books_inverted_index/part-00000 | python query_mapper.py | sort -k1,1 -k2,1 | python query_reducer.py
"""

from sys import stdin
import os
import ast
# both programs need to reference the same keys
keys = ['yours', 'you', 'yield', 'king', 'shield', 'young', 'yawned', 'yards']


###########
# RANKING #
###########
reducer_index = {}
for line in stdin:
    # guard against blank lines
    if len(line.split('\t')) < 3:
        continue

    word, count_and_book, listing = line.split('\t')
    count, book = count_and_book.split(':')

    if word not in reducer_index:
        reducer_index[word] = []

    reducer_index[word].append([int(count), book, listing])

# sort when we're done, DESC --> so highest frequency is first
for word in reducer_index:
    reducer_index[word].sort(reverse=True)


#############
# RETRIEVAL #
#############
# and finally ---> go find the results in the associated files
# iterate through each search term
for key in keys:

    print('======================================')
    print('     SEARCH TERM: --> "%s"' % key)
    print('======================================')

    # check if we have the key, at all
    if key in reducer_index:

        # get top 3 documents
        for idx in range(0, 3):

            # guard against out of bounds
            if idx > len(reducer_index[key]) - 1:
                break

            # otherwise, we can retrieve data!
            else:
                # index into the target file
                target_data = reducer_index[key][idx]

                # get the first line number
                line_data = ast.literal_eval(target_data[2])
                line_num = line_data[0]  # could slice to :n, to get the first `n` numbers

                #print(line_num + '\n\n')
                #print(target_data)
                #line_num = int(line_num)

                # get the filename
                fname = target_data[1]

                # get the directory
                dir_path = os.path.dirname(os.path.realpath(__file__))

                # concat full path for our file
                fpath = dir_path + '/books/' + fname

                # only the grab the context for lines right our around our target
                context = ""
                with open(fpath) as f:
                    for i, line in enumerate(f):
                        if i == line_num - 1:
                            context += '\t' + line
                        if i == line_num:
                            context += '\t' + line
                        if i == line_num + 1:
                            context += '\t' + line

                # and print our result!
                print('Result %d for search term ---> `%s`:\nTITLE: %s\n%s' % ((idx + 1), key, fname, context))


    # if we don't have the word, display this result for user
    else:
        print('------------------------')
        print('No results for word: "%s"' % key)
        print('------------------------')