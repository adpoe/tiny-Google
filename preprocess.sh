#!/bin/bash

# get the filename of all all files in current path
dir=/Users/tony/Documents/_LEARNINGS/CLOUD/tiny-Google/books_preprocess

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

done

# remove intermediate files created by sed, now that we're done
rm "$dir"/*.txt-e


# And now we have preprocessed files. Each book has its filename and then a tab in each line.
# This will make processing each book with an ID in MapReduce very simple.
# --> As a bonus:  SED works extremely quickly. Should only take less than 1 second total
#     to add this to all books.