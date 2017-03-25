#! /usr/bin/python
"""
 Usage: test with -->
    cat books_inverted_index/part-00000 | python query_mapper.py | sort -k1,1 -k2,1 | python query_reducer.py
"""

from sys import stdin
import os
import ast
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
# w(key, doc) = (1 + log2 freq(key,doc)) * log2 (N / n(doc))
# w(key, doc) is the weight of a word(key) in some doc
# freq(key, doc) is just the frequency of a word in some doc
# (N/n(doc)) where N = number of total docs, and n(doc) = number of docs the word appears in
# for more info : https://en.wikipedia.org/wiki/Tf%E2%80%93idf
def calc_weight(freq, doc_freq):

    #this is part calculation of idf which is inverse document frequency
    part_idf = 16.0/doc_freq
    idf = math.log(part_idf, 2)

    #this is calculation of term frequency
    tf = 1 + math.log(freq, 2)
    weight = idf*tf
    weight = round(weight, 6)

    #returns the weight of some word in given doc
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

        #The weight of the word in given doc based on the number of docs
        #it appears in and total number of docs.
        weight = calc_weight(freq, doc_freq)

        if doc not in weights_per_doc:
            weights_per_doc[doc] = [word, weight]
            total_weights[doc] = weight
        else:
            weights_per_doc[doc].append([word, weight])
            total_weights[doc] = total_weights[doc] + weight

#search term string
search_term = " "
#do all the calculations using rel_rank
for key in keys:
    if key in reducer_index:
        rel_rank(key)
search_term = search_term.join(keys)

#sort the weights in decending order for ease of access
sort_weights = sorted(total_weights.items(), key=lambda value: value[1], reverse=True)

###############################
# RELEVANCE RANKING RETRIEVAL #
###############################
print('================================================================================')
print('     SEARCH TERM: --> "%s"' % search_term)
print('================================================================================')

# split the term, to go through
search_list = search_term.split()

save_line_num = {}
#find if any words appear in the same context, in other words a phrase
for x in range(0, 3):

    #go through each word
    for some_word in search_list:
         #if there are an words at all
         if sort_weights:
             #find the word in index
             if some_word in reducer_index:
                 #get infor about the word
                 for target_data in reducer_index[some_word]:

                     #if it's the word from the book we are looking for
                     if target_data[1] == sort_weights[x][0]:

                         # get the first line number
                         line_data = ast.literal_eval(target_data[2])

                         #sort line data so, if it's a phrase the line numbers will be the same
                         line_data.sort()

                         #pick the first available line_num
                         #AKA the first place it appears at
                         line_num = line_data[0]  # could slice to :n, to get the first `n` numbers

                         #record the doc we are in
                         doc = target_data[1]

                         #create a tuple with line number and doc
                         target = (line_num, doc)

                         #if it's already not in our dictionary, add it to the dictionarry
                         #with prev tuple as the key
                         if target not in save_line_num:
                             #put the word at given tuple
                             save_line_num[(line_num, doc)] = [some_word]
                         else:
                             #if it line_num and doc tuple is alread there, it means the word is
                             #probably part of a phrase
                             save_line_num[(line_num, doc)].append(some_word)
         else:
             print("No words found!")

print_term = " "
#print the top 3 results from the weights_per_doc
for x in range(0, 3):
    print("\n")
    if sort_weights:
        #the total weight per doc, which is search_term[0]_weight + search_term[1]_weigth +..search_term[n]_weight
        #added some boldness to weight for aesthetics
        print_weight = ("Weight = %f"%(sort_weights[x][1]))
        print_weight = bcolors.BOLD + print_weight + bcolors.ENDC
        print("Result %d --> %s"%(x+1,print_weight))
        #print title
        cur_title = bcolors.OKBLUE+ bcolors.BOLD +  sort_weights[x][0] + bcolors.ENDC
        print("TITLE : %s\n" %(cur_title))

    for some_line in save_line_num:
        if some_line[1]==sort_weights[x][0]:

            #display what key words the context is for
            word_list = save_line_num[some_line]
            print_term = ", ".join(word_list)
            print("Earliest context found for terms : %s"%(print_term))
            print("---------------------------------------------------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------------------------")

            #get line number
            line_num = some_line[0]

            # get the filename
            fname = some_line[1]

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
                        context += '\t' + bcolors.OKGREEN + line + bcolors.ENDC #added color for aesthetics
                    if i == line_num:
                        context += '\t' + line
                    if i == line_num + 1:
                        context += '\t' + line
                    if i == line_num + 2:
                        context += '\t' + line
            #print the context around the words in the search term
            print(context)
            print("---------------------------------------------------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------------------------")



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
                            context += '\t' + bcolors.OKGREEN + line + bcolors.ENDC
                        if i == line_num:
                            context += '\t' + line
                        if i == line_num + 1:
                            context += '\t' + line
                        if i == line_num + 2:
                            context += '\t' + line

                # and print our result!

                #bold count for aesthetics
                occur = bcolors.BOLD + str(count) + bcolors.ENDC

                #color book title for aesthetics
                fname = bcolors.OKBLUE + bcolors.BOLD + fname + bcolors.ENDC

                print('Result %d for search term ---> `%s`:\nTITLE: %s\t >> Word Occurrences: %s << \n%s' %
                      ((idx + 1), key, fname, occur, context))


    # if we don't have the word, display this result for user
    else:
        print('------------------------------------')
        print('No results for word: "%s"' % key)
        print('------------------------------------')
