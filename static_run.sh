STREAM="hadoop jar  /usr/local/Cellar/hadoop/2.7.3/libexec/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -conf conf/hadoop-localhost.xml"

$STREAM \
  -D stream.num.map.output.key.fields=2 \
  -files inverted_index_mapper.py,\
inverted_index_reducer.py \
  -input books \
  -output books_inverted_index \
  -mapper inverted_index_mapper.py \
  -reducer inverted_index_reducer.py

