import os 
orgList=os.listdir('/home/parth/Desktop/matrices/')
orgList.sort()
for org in orgList:
    newName=org.replace('_adjMatrix','')
    oldFile = os.path.join('/home/parth/Desktop/matrices/', org)

    newFile = os.path.join('/home/parth/Desktop/matrices/',newName)
    # print(oldFile,newFile)
    os.rename(oldFile,newFile)

