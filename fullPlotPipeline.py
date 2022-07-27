import MatrixGenerationUserRepo
import createGML
import degreeDistribution

import os, time 

def matrixToPlot(org):
    print("========================================")
    print('Starting for '+org)
    flag=0
    # Step 1 - convert JSON to CSV
    # start1=time.time()
    # try:
    #     MatrixGenerationUserRepo.createMatrixByActivityType(org,activityType='starred')
    #     print('[Y] Matrix generation from JSON successful',end='')
    # except:
    #     print('[X] Matrix generation from JSON failed', end='')
    #     end1 = time.time()
    #     print(' in '+str(round(end1 - start1)) + ' sec')
    #     return False
    # end1 = time.time()
    # print(' in '+str(round(end1 - start1)) + ' sec')
    
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

orgList = os.listdir('latest-matrix')
orgList.sort()
# print(orgList)
# orgList=['99designs.json']
for org in orgList: 
    org = org.replace('.csv', '')
    # print(org)
    resp=matrixToPlot(org)
    if resp==False:
        print("[X] ERROR")
    else:
        print("[Y] NO ERROR")
    print("========================================")

print("========================================")
