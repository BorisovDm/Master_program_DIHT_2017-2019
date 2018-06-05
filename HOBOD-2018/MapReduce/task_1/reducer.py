#!/usr/bin/env python3

from collections import defaultdict
import heapq
import sys
sys.stdin = open(sys.stdin.fileno(), encoding='utf-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)

TOP_PERMUTATIONS = 10
TOP_RECORDS = 5

q = []
d = defaultdict(int)
last_sorted_word, count = None, 0

for line in sys.stdin:
    sorted_word, word = line.strip().split('\t')
    if last_sorted_word and sorted_word != last_sorted_word:
        popular_words = ''
        for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True)[:TOP_RECORDS]:
            popular_words += "%s:%d;" % (k, v)

        if len(q) < TOP_PERMUTATIONS:
            heapq.heappush(q, (count, "%s\t%s" % (last_sorted_word, popular_words)))
        elif count > q[0][0]:
            heapq.heapreplace(q, (count, "%s\t%s" % (last_sorted_word, popular_words)))

        d = defaultdict(int)
        last_sorted_word, count = sorted_word, 1
        d[word] += 1
    else:
        last_sorted_word, count = sorted_word, count + 1
        d[word] += 1

if last_sorted_word:
    popular_words = ''
    for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True)[:TOP_RECORDS]:
        popular_words += "%s:%d;" % (k, v)

    if len(q) < TOP_PERMUTATIONS:
        heapq.heappush(q, (count, "%s\t%s" % (last_sorted_word, popular_words)))
    elif count > q[0][0]:
        heapq.heapreplace(q, (count, "%s\t%s" % (last_sorted_word, popular_words)))

for top_statistics in q:
    sorted_word, popular_words = top_statistics[1].strip().split('\t', 1)
    print("%s\t%d\t%s" % (sorted_word, top_statistics[0], popular_words))