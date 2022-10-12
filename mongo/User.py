
from turtle import update
import requests
import json 
import sys
import os

sys.path.append('../step2_obtainMemberActivity')
sys.path.append('../extra/misc')

import repo


def getuserlistfororg():
   
    import apiRobin
    from helper_methods import getRandomAPIToken
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    reqUrl='https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user'

    orglist=os.listdir('/Users/mananvadaliya/Documents/github-recommendation-project-main/step2_obtainMemberActivity/data/test/reddit.json')
    orgList = {x.replace('.json', '') for x in orgList}
    orgList=sorted(orgList)

    for org in orgList:
        pageNo=1
        userList=[]
        while(True):
            response = requests.get(reqUrl+org+'/repos?page='+str(pageNo),headers=headers).json()
            if(len(response)==0):
                break
            userList.extend(response)
            pageNo=pageNo+1
    with open('userList/'+org+'.json','w') as f:
            json.dump(userList,f)
    print(org, len(userList))
        




    # def getRepofromUser(userList[],org):
        #return repo



    def getRelevantFields(repo):
   #(repo) --> returned repo from getRepofromUser(userList[],org):
    with open('userList/'+org+'.json','r') as f: 
        userList=json.load(f)
        updatedList=[]
       
        reqKeys = ['language','collaboraters_id','commits' ]
        for d in userList:
            user = {}
            for key in reqKeys:
                user[key]=d.get(key)
            user.update(user)
            updatedList.append(user)
            
    return updatedList