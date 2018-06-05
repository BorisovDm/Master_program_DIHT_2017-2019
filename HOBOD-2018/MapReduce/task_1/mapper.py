#!/usr/bin/env python3

import sys
import re

sys.stdin = open(sys.stdin.fileno(), encoding='utf-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)

for line in sys.stdin:
    for word in re.sub('[.,:?!;]', '', line).lower().split():
        if len(word) < 3: continue
        print("%s\t%s" % (''.join(sorted(word)), word))