#!/usr/bin/env bash
dir=${PWD}

rm -r "$dir"/books_preprocess/*    # remove all files, but not directory itself
rm -r "$dir"/books_inverted_index  # remove all files AND directory
rm -r "$dir"/query_result          # remove all files AND directory
