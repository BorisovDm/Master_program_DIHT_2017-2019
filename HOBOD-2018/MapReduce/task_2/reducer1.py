#!/usr/bin/env python3

import datetime
import sys

sys.stdin = open(sys.stdin.fileno(), encoding='utf-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)

last_url, first_mention, last_mention = None, None, None

for line in sys.stdin:
    url, timestamp, diff_time = line.strip().split('\t')
    timestamp = int(timestamp)
    logout_time = timestamp + int(diff_time)

    if not last_url:
        last_url, first_mention, last_mention = url, timestamp, logout_time
        continue

    if url == last_url:
        first_mention = min(first_mention, timestamp)
        last_mention = max(last_mention, logout_time)
    else:
        last_url = last_url.split('://')[1].split('/')[0]
        if last_url.startswith('www.'):
            last_url = last_url[4:]

        t1 = datetime.datetime.fromtimestamp(first_mention)
        t1 = datetime.datetime(t1.year, t1.month, t1.day)

        t2 = datetime.datetime.fromtimestamp(last_mention)
        t2 = datetime.datetime(t2.year, t2.month, t2.day)

        print("%s\t%d" % (last_url, (t2 - t1).days + 1))
        last_url, first_mention, last_mention = url, timestamp, logout_time

if last_url:
    last_url = last_url.split('://')[1].split('/')[0]
    if last_url.startswith('www.'):
        last_url = last_url[4:]

    t1 = datetime.datetime.fromtimestamp(first_mention)
    t1 = datetime.datetime(t1.year, t1.month, t1.day)

    t2 = datetime.datetime.fromtimestamp(last_mention)
    t2 = datetime.datetime(t2.year, t2.month, t2.day)
    print("%s\t%d" % (last_url, (t2 - t1).days + 1))