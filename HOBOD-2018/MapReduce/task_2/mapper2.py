#!/usr/bin/env python3

import sys
sys.stdin = open(sys.stdin.fileno(), encoding='utf-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)

for line in sys.stdin:
    print("%s\t1" % line.strip())