import os 
orgList=os.listdir('matrix_user_repo/starred/adjacency/')
orgList.sort()
for org in orgList:
    newName=org.replace('_adjMatrix','')
    oldFile = os.path.join('matrix_user_repo/starred/adjacency/', org)

    newFile = os.path.join('matrix_user_repo/starred/adjacency/', newName)
    # print(oldFile,newFile)
    os.rename(oldFile,newFile)

