#!/usr/bin/env python3

import heapq
import sys

sys.stdin = open(sys.stdin.fileno(), encoding='utf-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)

TOP_RECORDS = 10
q = []
last_url, url_days, url_count = None, 0, 0

for line in sys.stdin:
    url, days, count = line.strip().split('\t')

    if last_url and url != last_url:
        average = url_days / url_count

        if len(q) < TOP_RECORDS:
            heapq.heappush(q, (average, last_url))
        elif average > q[0][0]:
            heapq.heapreplace(q, (average, last_url))

        last_url, url_days, url_count = url, int(days), int(count)
    else:
        last_url, url_days, url_count = url, url_days + int(days), url_count + int(count)

if last_url:
    average = url_days / url_count

    if len(q) < TOP_RECORDS:
        heapq.heappush(q, (average, last_url))
    elif average > q[0][0]:
        heapq.heapreplace(q, (average, last_url))

for dat in sorted(q, key=lambda x: x[0], reverse=True):
    print("%s\t%f" % (dat[1], dat[0]))