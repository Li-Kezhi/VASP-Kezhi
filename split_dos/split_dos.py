#!/usr/bin/python

'''
Split DOSCAR into seperate files

Assuming that LORBIT = 11
The script should be put at the working respiratory
'''

__author__ = "LI Kezhi" 
__date__ = "$2016-10-18$"
__version__ = "1.0"

lineNum = 0
rows = 0    # the total number of rows

fileNum = 0
isNewStart = True    # Flag: beginning of a single file

i = -1
def count():
    # Output an increasing integer until i == rows
    i = 0
    while True:
        i += 1
        yield i
index = count()

for line in open('DOSCAR', 'r'):
    if lineNum == 5:    # pass the header
        splitting = line.split()
        rows = int(splitting[2])
        isNewStart = False
        file = open('DOS' + str(fileNum), 'w')
    elif lineNum > 5:
        if isNewStart:
            file = open('DOS' + str(fileNum), 'w')
            isNewStart = False
            continue    # pass the header
        file.write(line)
        if index.next() % rows == 0:    # end of data
            fileNum += 1
            isNewStart = True
            file.close()
    lineNum += 1

print ('%d DOS file(s) have been splitted named as DOS0, DOS1...' % fileNum)