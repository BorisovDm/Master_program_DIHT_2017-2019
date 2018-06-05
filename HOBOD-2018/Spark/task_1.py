#!/usr/bin/env python3

import re
import sys
from pyspark import SparkContext, SparkConf
from operator import add

reload(sys)
sys.setdefaultencoding('utf8')

WORD = 'narodnaya'

def parse_pairs(line):

    words = re.sub('[.,:?!;0-9|()//]', ' ', line).lower().split()
    result = []

    for i in range(len(words) - 1):
        if words[i] == WORD:
            result.append('%s_%s' % (words[i], words[i + 1]))
    return result


if __name__ == "__main__":
    sc = SparkContext(conf=SparkConf().setAppName("spark_hw_task_1").setMaster("yarn-client"))

    pairs = sc.textFile("%s" % sys.argv[1])\
                .flatMap(parse_pairs)\
                .map(lambda x: (x, 1))\
                .reduceByKey(add)\
                .sortByKey()\
                .collect()

    for val in pairs:
        print('%s\t%d' % val)