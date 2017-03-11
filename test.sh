cat books_preprocess/*.txt | python inverted_index_mapper.py | sort -k1,1 | python inverted_index_reducer.py
