#!/bin/bash

# define input directory
booksdir=${PWD}/books

# define working directory
dir=${PWD}/books_preprocess

# move input directory books to working directory
cp -r "$booksdir"/* $dir

# get the filename of all all files in target path
#dir=${PWD}/books_preprocess  <-- test that this works, when we get there
#dir=/Users/tony/Documents/_LEARNINGS/CLOUD/tiny-Google/books_preprocess

# iterate through all files in directory
for entry in "$dir"/*
do
  # print so users knows what files were updated
  echo "$entry"

  # grab only the file name, and print it
  fname="${entry##*/}"
  echo "$fname"

  # using sed, add the file name a s prefix to EVERY line of the entry
  sed -i -e 's/^/'$fname'\\t/' $entry

  # add line numbers, using unix nl command
  # (need to add new file for output, so mark it as '_preprocessed')
  nl $entry > "$entry"_preprocessed
done

# remove intermediate files created by `sed` and `nl`, now that we're done
rm "$dir"/*.txt-e
rm "$dir"/*.txt

# change file names back, so that input fnames match output
for f in "$dir"/*.txt_preprocessed; do
  mv -- "$f" "${f%.txt_preprocessed}.txt"
done

# And now we have preprocessed files. Each book has its filename and then a tab in each line.
# This will make processing each book with an ID in MapReduce very simple.
# --> As a bonus:  SED works extremely quickly. Should only take less than 1 second total
#     to add this to all books.