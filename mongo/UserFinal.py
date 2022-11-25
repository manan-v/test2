
from turtle import update
import requests
import json 
import sys
import os

sys.path.append('../step2_obtainMemberActivity')
sys.path.append('../extra/misc')

import repo.repo as repo
import apiRobin
from helper_methods import getRandomAPIToken

def getuserlistfororg():
   
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    reqUrl='https://api.github.com/orgs/'

    orglist=os.listdir('/Users/mananvadaliya/Documents/github-recommendation-project-main/step2_obtainMemberActivity/data/test/reddit.json')
    orgList = {x.replace('.json', '') for x in orgList}
    orgList=sorted(orgList)

    for org in orgList:
        pageNo=1
        userList=[]
        while(True):
            response = requests.get(reqUrl+org+'/members?page='+str(pageNo),headers=headers).json() 
            if(len(response)==0):
                break
            #login id  username
            for user in response:
                userId={}
                userId[user]=response.get(login) 
            #with open('../userList/' + org + '.json','r' ) as f:
            userList.extend(userId)
            userList.extend(response)
            pageNo=pageNo+1
    with open('userList/'+org+'.json','w') as f:
            json.dump(userList,f)
    print(org, len(userList))

        
def getRepofromUser(userList):
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    reqUrl='https://api.github.com/users'

    for user in userList:
        pageNo=1
        repoList=[]
        # Get primary data
        while(True):
            response = requests.get(reqUrl+user+'/repos?page='+str(pageNo),headers=headers).json()
            if(len(response)==0):
                break
            repoList.extend(response)
            pageNo=pageNo+1
        
        # Get list of contributors
        # repoList=getContributorForRepo(repoList)

        with open('../repoList/'+user+'.json','w') as f:
            json.dump(repoList,f)
        print(user, len(repoList))
         

def getRelevantFields(repoList):
#(repo) --> returned repo from getRepofromUser(userList[],org):
    with open('userList/'++'.json','r') as f: 
        userList=json.load(f)
        updatedList=[]

        reqKeys = ['language','collaboraters_id','commits' ]
        for d in userList:
            user = {}
            for key in reqKeys:
                user[key]=d.get(key)
            user.update(user)
            updatedList.append(user)
        
