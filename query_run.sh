#!/usr/bin/env bash
STREAM="hadoop jar  /usr/local/Cellar/hadoop/2.7.3/libexec/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -conf conf/hadoop-localhost.xml" \

$STREAM \
  -files query_mapper.py,\
query_reducer.py \
  -input books_inverted_index \
  -output query_result \
  -mapper query_mapper.py \
  -reducer query_reducer.py

