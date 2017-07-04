#!/usr/bin/env python
# # -*- coding:utf-8 -*-

"""
Add "T/F" mark in POSCAR file
"""

__author__ = "LI Kezhi"
__date__ = "$2017-07-04$"
__version__ = "0.0.2"

Z_BOUNDARY = None # When z >= Z_BOUNDARY, add "T" marks, else add "F" marks
if Z_BOUNDARY is None:
    Z_BOUNDARY = raw_input('Please enter the z value for fixing boundary:')

output = open('POSCARout', 'w')
with open('POSCAR', 'r') as f:
    isCrystalSize = False
    isEndOfCrystalSize = False
    isElementsLine = False
    isEndOfElemtnsLine = False
    isCoordinate = False

    for line in f:
        splitted = line.split()

        # Find the beginning of crystal size data
        if len(splitted) >= 3:
            for i, item in enumerate(splitted):
                if i == 3:
                    break
                try:
                    float(item)
                except ValueError:
                    break
                if i == 2:
                    isCrystalSize = True

        # Find the end of crystal size data
        if isCrystalSize is True:
            if len(splitted) < 3:
                isEndOfCrystalSize = True
            else:
                for i, item in enumerate(splitted):
                    if i == 3:
                        break
                    try:
                        float(item)
                    except ValueError:
                        isEndOfCrystalSize = True
                        isCrystalSize = True

        # Find the beginning of elements data
        if isEndOfCrystalSize and not isEndOfElemtnsLine:
            for item in splitted:
                preStatus = isElementsLine
                try:
                    float(item)
                except ValueError:
                    isElementsLine = True
                    break
                finally:
                    if preStatus: # isElementsLine was set True before
                        isEndOfElemtnsLine = True

        # Find the beginning of coordination data
        if isEndOfElemtnsLine:
            if splitted[0][0] in 'dDkKcC':
                isCoordinate = True
                output.write('Selective dynamics\n')
                output.write(line)
                continue

        # Actions
        if not isCoordinate:
            output.write(line)
        else:
            x, y, z = line.rstrip().split()
            output.write(line.rstrip())
            if z < Z_BOUNDARY:
                output.write(' F F F\n')
            else:
                output.write(' T T T\n')
