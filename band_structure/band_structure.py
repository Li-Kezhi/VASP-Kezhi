#!/usr/bin/env python
'''
Plot band structure

The script should be put at the working respiratory
'''

__author__ = "LI Kezhi"
__date__ = "$2016-10-23$"
__version__ = "1.1"

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
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 +
        (point1[2] - point2[2])**2)

# Read KPOINTS to get critical k-points
fileName = 'KPOINTS'
kpoints = []
isKpointsBeginning = False
with open(fileName, 'r') as f:
    for line in f:
        splitting = [item for item in line.split() if item != '']
        if splitting != [] and splitting[0][0] in 'Rr':  # find R(r)eciprocal
            isKpointsBeginning = True
            continue
        if isKpointsBeginning == True:
            if splitting != []:
                kpoint = [
                    float(splitting[0]), 
                    float(splitting[1]), 
                    float(splitting[2])
                ]
                if kpoint not in kpoints:
                    kpoints.append(kpoint)


# Read EIGENVAL
fileName = 'EIGENVAL'

lineNum = 0
kpointMark = []
bandEnergy = {}
bandOccupancy = {}
kpointDistance = []
with open(fileName, 'r') as f:
    for line in f:
        if lineNum == 5:  # header
            bandNum = int(line.split()[2])
            kpointNum = int(line.split()[1])
            # Initiate bandEnergy and bandOccupancy
            for i in xrange(bandNum):
                bandEnergy[i] = []
                bandOccupancy[i] = []

        if lineNum >= 7:
            currentIndexLine = indexLine.next()
            if currentIndexLine % (bandNum + 2) == 0:  # header
                splitting = [item for item in line.split() if item != '']
                kpoint = [
                    float(splitting[0]), 
                    float(splitting[1]), 
                    float(splitting[2])
                ]
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
                splitting = [item for item in line.split() if item != '']
                splitting0 = int(splitting[0])
                bandEnergy[splitting0 - 1].append(float(splitting[1]))
                bandOccupancy[splitting0 - 1].append(float(splitting[2]))

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

Y = np.zeros_like(X)  # add Fermi reference line
plt.plot(X, Y)

for kpoint in kpointMark:  # add critical k-points line
    plt.axvline(x=X[kpoint], color='black', linestyle='dotted')

plt.ylabel('E - Ef (eV)')

plt.show()