#!/usr/bin/python

'''
Plot band structure

The script should be put at the working respiratory
'''

__author__ = "LI Kezhi" 
__date__ = "$2016-10-19$"
__version__ = "1.0"

import numpy as np
import matplotlib.pyplot as plt


def count():
    # Output an increasing integer
    i = 0
    while True:
        yield i
        i += 1
indexLine = count()

def distance(point1, point2):
    '''
    Calculate the distance between two points
    Input: two points as form of list
    Example: point1 = [0.0, 0.5, 0.0]
    '''
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

# Read KPOINTS to get critical k-points
file = 'KPOINTS'
kpoints = []
isKpointsBeginning = False
for line in open(file, 'r'):
    splitting = line.split()
    if splitting != [] and splitting[0][0] in 'Rr':    # find reciprocal/Reciprocal
        isKpointsBeginning = True
        continue
    if isKpointsBeginning == True:
        if splitting != []:
            kpoint = [float(splitting[0]), float(splitting[1]), float(splitting[2])]
            if not kpoint in kpoints:
                kpoints.append(kpoint)


# Read EIGENVAL
file = 'EIGENVAL'

lineNum = 0
kpointMark = []
bandEnergy = {}
bandOccupancy = {}
kpointDistance = []
for line in open(file, 'r'):
    if lineNum == 5:    # header
        bandNum = int(line.split()[2])
        kpointNum = int(line.split()[1])
        # Initiate bandEnergy and bandOccupancy
        for i in xrange(bandNum):
            bandEnergy[i] = []
            bandOccupancy[i] = []

    if lineNum >= 7:
        currentIndexLine = indexLine.next()
        if currentIndexLine % (bandNum + 2) == 0:    # header
            splitting = line.split()
            kpoint = [float(splitting[0]), float(splitting[1]), float(splitting[2])]
            if kpoint in kpoints:
                kpointMark.append(currentIndexLine / (bandNum + 2))
            # Calculate respiracal distance
            if 'lastKpoint' in locals().keys():
                kpointDistance.append(distance(lastKpoint, kpoint))
                lastKpoint = kpoint
            else:
                kpointDistance.append(0)
                lastKpoint = kpoint
        elif currentIndexLine % (bandNum + 2) < (bandNum + 1):
            splitting = line.split()
            bandEnergy[int(splitting[0]) - 1].append(float(splitting[1]))
            bandOccupancy[int(splitting[0]) - 1].append(float(splitting[2]))

    lineNum += 1

# Plotting
X = np.zeros(kpointNum)
totalDistance = sum(kpointDistance)
sumDistance = 0
for i in xrange(kpointNum):
    X[i] = (sumDistance + kpointDistance[i]) / totalDistance
    sumDistance += kpointDistance[i]
for i in xrange(bandNum):
    plt.plot(X, bandEnergy[i])

Y = np.zeros_like(X)    # add Fermi reference line
plt.plot(X, Y)

for kpoint in kpointMark:    # add critical k-points line
    plt.axvline(x = X[kpoint], color = 'black', linestyle = 'dotted')

plt.ylabel('E - Ef (eV)')

plt.show()