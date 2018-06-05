from __future__ import division
from pyspark import SparkConf, SparkContext
from operator import add
from math import log
import re


STOP_WORDS_FILE = '/datasets/stop_words_en.txt'
WIKI_FILE = '/data/wiki/en_articles_part/articles-part'


def parse_article(line):
    try:
        _, text = unicode(line.rstrip()).split('\t', 1)
        text = re.sub("^\W+|\W+$", "", text, flags=re.UNICODE).lower()
        words = re.split("\W*\s+\W*", text, flags=re.UNICODE)
        return [word for word in words if word not in stop_words]
    except ValueError as e:
        return []
        
        
def get_pairs(words):
    return ['%s_%s' % (a, b) for a, b in zip(words, words[1:])]
    
    
def npmi(pair):
    left, right = unicode(pair[0]).split('_', 1)
    p_left = word_count[left] / total_words_number
    p_right = word_count[right] / total_words_number
    p_pair =  pair[1] / total_pairs_number
    value = log(p_left * p_right / p_pair) - 1
    return (pair[0], value)


with open(STOP_WORDS_FILE) as f:
    stop_words = set(word.strip().lower() for word in f.readlines())
    
sc = SparkContext(conf=SparkConf().setAppName("spark_hw_task_2").setMaster("yarn-client"))

wiki = sc.textFile(WIKI_FILE) \
                    .map(parse_article) \
                    .cache()
                  
word_count = wiki \
                    .flatMap(lambda x: x) \
                    .map(lambda x: (x, 1)) \
                    .reduceByKey(add) \
                    .collectAsMap()

total_words_number = sum(word_count.values())
    
pairs = wiki \
                    .flatMap(get_pairs) \
                    .map(lambda x: (x, 1)) \
                    .reduceByKey(add) \
                    .filter(lambda x: x[1] > 499) \
                    .cache()
                    
total_pairs_number = pairs.count()
    
top = pairs \
                    .map(npmi) \
                    .sortBy(lambda x: x[1])\
                    .take(39)
                    
for pair, _ in top:
    print pair
