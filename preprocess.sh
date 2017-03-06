#!/bin/bash
# get the filename of all all files in current path
dir=/Users/tony/Documents/_LEARNINGS/CLOUD/tiny-Google/books_preprocess
for entry in "$dir"/*
do
  echo "$entry"
  fname="${entry##*/}"
  echo "$fname"
  # works but makes a file with -e appended in same directory
  sed -i -e 's/^/'$fname'\\t/' $entry
  #awk '$0="$fname"$0'
  # add into a new folder with preprocessed data
  #sed -e 's/^/prefix/' $entry > "$dir"/preprocessed/"$entry"
done
