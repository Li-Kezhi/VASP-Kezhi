'''
Add "T" mark in POSCAR file
'''

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
                output.write(line)
                continue

        # Actions
        if not isCoordinate:
            output.write(line)
        else:
            output.write(line.rstrip())
            output.write(' T T T\n')
