import createGML
import degreeDistribution

import os
import time


def matrixToPlot(org):
    print("========================================")
    print('Starting for '+org)

    # Step 2 - convert CSV to GML
    start2 = time.time()
    try:
        createGML.createGML(org)
        print('[Y] GML Conversion successful', end='')
    except:
        print('[X] GML Conversion failed', end='')
        end2 = time.time()
        print(' in '+str(round(end2 - start2)) + ' sec')
        return False
    end2 = time.time()
    print(' in '+str(round(end2 - start2)) + ' sec')

    # Step 3 - Calc degree distribution and plot
    start3 = time.time()
    try:
        degreeDistribution.calcDegreeAndPlot(org)
        print('[Y] Degree computation and plot successful', end='')
    except:
        print('[X] Degree computation and plot failed', end='')
        end3 = time.time()
        print(' in '+str(round(end3 - start3)) + ' sec')
        return False
    end3 = time.time()
    print(' in '+str(round(end3 - start3)) + ' sec')

    return True


orgList = os.listdir('latest-matrix/matrix')
orgList.sort()
# print(orgList)
# orgList=['99designs.json']
for org in orgList:
    org = org.replace('.csv', '')
    print(org)
    resp = matrixToPlot(org)
    print("========================================")
    if resp == False:
        print("[X] ERROR")
    else:
        print("[Y] NO ERROR")
print("========================================")
