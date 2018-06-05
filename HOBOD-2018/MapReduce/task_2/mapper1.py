#!/usr/bin/env python3

import sys
sys.stdin = open(sys.stdin.fileno(), encoding='utf-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)

for line in sys.stdin:
    data = line.strip().split('\t')
    print("%s\t%s\t%s" % (data[2], data[1], data[3][10:]))