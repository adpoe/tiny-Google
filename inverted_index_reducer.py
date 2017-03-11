#! /usr/bin/python
"""
 Usage: test with -->
 cat books_preprocess/*.txt | python inverted_index_mapper.py | sort -k1,1 | python inverted_index_reducer.py
"""

from sys import stdin

# create data structures to store:
count_totals = {}   # --> word counts per document, total
occurrence_indices = {}  # --> the lines where each occurrence appears, in that document

# take each line one at a time from Hadoop Streaming
for line in stdin:

    # split input data into the word itself and the metadata for each book
    word, book_data = line.split('\t')

    # initialize our dictionaries, to ensure there are no invalid key exceptions
    count_totals.setdefault(word, {})
    occurrence_indices.setdefault(word, {})

    # books are separated by a ',' in our data structure,
    # so split on commas to get data related to each book,
    # in series
    for line_data in book_data.split(','):
        book_name, count, line_num = line_data.split(':')
        count = int(count)
        line_num = int(line_num)

        # handle count index
        count_totals[word].setdefault(book_name, 0)
        count_totals[word][book_name] += count

        # handle occurrence index
        occurrence_indices[word].setdefault(book_name, [])
        occurrence_indices[word][book_name].append(line_num)


# now that we've processed stdin and tallied occurrences + counts
# next step is to combine this data into one structure,
# then output it
for word in count_totals:
    # use list comprehension for each word, to pull our data into same structure,
    # before we output to stdout
    occurence_list = ["%s:%d:%s" % (book_name, count_totals[word][book_name],
                                    str(occurrence_indices[word][book_name]))
                                        for book_name in count_totals[word]]

    # separate data for each BOOK by a `;` --> can't use a `,` ==> because we have a list embedded
    # within this structure as well.
    # using a `;`, will ensure we can split by book easily, and on a unique index
    # when we run a query
    book_data = ';'.join(occurence_list)
    # and --> finally, print to stdout
    print('%s\t%s' % (word, book_data))
