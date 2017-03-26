#!/usr/bin/env python
'''
Split DOSCAR into seperate files

Assuming that LORBIT = 11
The script should be put at the working respiratory
'''

from __future__ import print_function

__author__ = "LI Kezhi"
__date__ = "$2017-02-26$"
__version__ = "1.1.1"

rows = 0  # the total number of rows

fileNum = 0
isNewStart = True  # Flag: beginning of a single file

i = -1
def count():
    # Output an increasing integer until i == rows
    i = 0
    while True:
        i += 1
        yield i


index = count()

with open('DOSCAR', 'r') as f:
    lineNum = 0
    for line in f:
        if lineNum == 5:  # pass the header
            splitting = [item for item in line.split() if item != '']
            rows = int(splitting[2])
            isNewStart = False
            f = open('DOS' + repr(fileNum), 'w')
        elif lineNum > 5:
            if isNewStart:
                f = open('DOS' + repr(fileNum), 'w')
                isNewStart = False
                continue  # pass the header
            f.write(line)
            if index.next() % rows == 0:  # end of data
                fileNum += 1
                isNewStart = True
                f.close()
        lineNum += 1

print('%d DOS file(s) have been splitted named as DOS0, DOS1...' % fileNum)
