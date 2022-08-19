import json
import pandas as pd

def colAndRow(org, activityType,path='../step2_obtainMemberActivity/data/test/'):
    path=path+org+'.json'
    userSet = set([])
    repoSet = set([])
    orgJSON = json.load(open('../step2_obtainMemberActivity/data/test/'+org+'.json'))
    for user in orgJSON:
        userSet.add(user)
        repoSet.update(orgJSON[user][activityType])
    return list(userSet), list(repoSet),orgJSON

def createBaseDf(userList,repoList):
    userList.sort()
    repoList.sort()
    baseDf = pd.DataFrame({}, columns=repoList, index=userList).fillna(0)
    return baseDf

def fillDf(orgJSON, baseDf, activityType):
    for user in baseDf.index:
        for repo in baseDf.columns:
            if(repo in orgJSON[user][activityType]):
                baseDf.loc[user,repo]=1
    return baseDf

def generateMatrix(org,activityType):
    userList, repoList, orgJSON = colAndRow(org, activityType)
    baseDf = createBaseDf(userList, repoList)
    finalDf = fillDf(orgJSON, baseDf, activityType)
    finalDf.to_csv('data/matrix_user_repo/'+activityType+'/'+org+'.csv', sep=',')

orgList = ['yeebase']
activityList=['starred','subscriptions']
for org in orgList:
    for activity in activityList:
        generateMatrix(org,activity)