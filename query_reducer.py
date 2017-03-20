#! /usr/bin/python
"""
 Usage: test with -->
    cat books_inverted_index/part-00000 | python query_mapper.py | sort -k1,1 -k2,1 | python query_reducer.py
"""

from sys import stdin
import os
import ast
import math

# both programs need to reference the same keys
#keys = ['yours', 'you', 'yield', 'king', 'shield', 'young', 'yawned', 'yards', 'xfas']
dir_path = os.path.dirname(os.path.realpath(__file__))
keywords_file = dir_path + '/search_keywords.txt'
with open(keywords_file) as f:
    keywords = f.read()
    keys = ast.literal_eval(keywords)





###########
# RANKING #
###########
reducer_index = {}
rel_index = {}
for line in stdin:
    # guard against blank lines
    if len(line.split('\t')) < 3:
        continue

    word, count_and_book, listing = line.split('\t')
    count, book = count_and_book.split(':')

    if word not in reducer_index:
        reducer_index[word] = []
        rel_index[word] = []

    reducer_index[word].append([int(count), book, listing])
    rel_index[word].append([int(count), book])

# sort when we're done, DESC --> so highest frequency is first
for word in reducer_index:
    reducer_index[word].sort(reverse=True)

# use algorithm to calculate the weight of a word in a doc
def calc_weight(freq, doc_freq):

    part_idf = 16.0/doc_freq
    idf = math.log(part_idf, 2)
    tf = 1 + math.log(freq, 2)
    weight = idf*tf
    weight = round(weight, 6)
    return weight

weights_per_doc = {}
total_weights = {}
##########################
#RELEVENCE RANKING SYSTEM#
##########################
def rel_rank(word):
    #number of docs the word appears in
    doc_freq = len(rel_index[word])

    for temp_book in rel_index[word]:
        #number of times the term appears in given doc
        freq = temp_book[0]

        #doc name -> book name
        doc = temp_book[1]

        #the weight of the word in given doc based on the number of docs
        #it appears in and total number of docs
        weight = calc_weight(freq, doc_freq)

        if doc not in weights_per_doc:
            weights_per_doc[doc] = [word, weight]
            total_weights[doc] = weight
        else:
            weights_per_doc[doc].append([word, weight])
            total_weights[doc] = total_weights[doc] + weight

#search term string
search_term = ""
#do all the calculations using rel_rank
for key in keys:
    rel_rank(key)
    search_term = search_term + key+ " "
sort_weights = sorted(total_weights.items(), key=lambda value: value[1], reverse=True)

###############################
# RELEVANCE RANKING RETRIEVAL #
###############################
print('================================================================================')
print('     SEARCH TERM: --> "%s"' % search_term)
print('================================================================================')
search_list = search_term.split()
for x in range(0, 3):
    print("\n")
    print("Result %d --> Weight = %f"%(x+1,sort_weights[x][1]))
    print("TITLE : %s" %(sort_weights[x][0]))
    for some_word in search_list:
        for target_data in reducer_index[some_word]:
            if target_data[1] == sort_weights[x][0]:
                # get the first line number
                line_data = ast.literal_eval(target_data[2])
                line_num = line_data[0]  # could slice to :n, to get the first `n` numbers
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
                        if i == line_num - 2:
                            context += '\t' + line
                        if i == line_num - 1:
                            context += '\t' + line
                        if i == line_num:
                            context += '\t' + line
                        if i == line_num + 1:
                            context += '\t' + line
                        if i == line_num + 2:
                            context += '\t' + line

                print(context)


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

                # get word occurrences
                count = reducer_index[key][idx][0]

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
                        if i == line_num - 2:
                            context += '\t' + line
                        if i == line_num - 1:
                            context += '\t' + line
                        if i == line_num:
                            context += '\t' + line
                        if i == line_num + 1:
                            context += '\t' + line
                        if i == line_num + 2:
                            context += '\t' + line

                # and print our result!
                print('Result %d for search term ---> `%s`:\nTITLE: %s\t >> Word Occurrences: %d << \n%s' %
                      ((idx + 1), key, fname, count, context))


    # if we don't have the word, display this result for user
    else:
        print('------------------------------------')
        print('No results for word: "%s"' % key)
        print('------------------------------------')
