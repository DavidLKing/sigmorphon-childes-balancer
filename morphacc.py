#!/usr/bin/env python3

import sys

correct = 0
total = 0

for l1, l2 in zip(open(sys.argv[1], 'r').readlines(), 
                  open(sys.argv[2], 'r').readlines()):
    if l1 == l2:
        correct += 1
    total += 1

print("Accuracy:", correct / total)
