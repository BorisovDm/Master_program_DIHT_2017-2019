from pyspark.streaming import StreamingContext
from pyspark import SparkContext

from operator import add
import re

 
sc = SparkContext(master='local[4]')
ssc = StreamingContext(sc, batchDuration=10)
 
dstream = ssc.socketTextStream(hostname='127.0.0.1', port=9999)
 
result = dstream \
    .flatMap(lambda line: re.split("\W*\s+\W*", line, flags=re.UNICODE)) \
    .filter(lambda word: len(word) > 0) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(add)

def print_word_count(rdd):
    for val in rdd:
        print('%s\t%d' % val)

dstream.filter(lambda x: False).pprint()
result.foreachRDD(lambda rdd: print_word_count(rdd.collect()))

ssc.start()
ssc.awaitTermination()
