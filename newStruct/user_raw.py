import requests
import json
import os
import apiRobin
import helper_methods
from repo_raw import members

# Get list of repos where user contributes
# https://api.github.com/users/USERNAME/repos
def contributing(user,headers):
    contributingUrl='https://api.github.com/users/'+user+'/repos'
    pageNo=1
    contributingRepos={}
    while(True):
        contributionResponse=requests.get(contributingUrl+'?page='+str(pageNo),headers=headers).json()
        if(len(contributionResponse)==0):
            break
        for contribution in contributionResponse:
            contributingRepos[contribution['name']]=contributionDetails(user,contribution['name'],headers)
        pageNo+=1
    return contributingRepos

# Get further details for contributions
    # https://api.github.com/repos/USERNAME/REPO/commits , get `sha`
    # -> https://api.github.com/repos/USERNAME/REPO/commits/SHA, 
    # get `sha`
    # get `committer.author.date`
    # get `stats`
    # get `file['filename'] for file in files`
# get a repo list of the spesific orgs
def repos(org,headers):
    orgUrl = 'https://api.github.com/orgs/'+org+'/repos'
    repos=[]
    pageNo=1
    while(True):
        repoResponse=requests.get(orgUrl+'?page='+str(pageNo), headers=headers).json()
        if(len(repoResponse)==0):
            break
        pageNo=pageNo+1
        for repo in repoResponse:
            repos.append(repo['name'])
    return repos

# Get list of repos where user is watching
# https://api.github.com/users/USERNAME/subscriptions
def coommitDetails(USERNAME,headers):   
    # USERNAME = 'manan-v'
    # commitsDet = []
    pageNo = 1
    repo ='OS'
    CommDetails=[]
    
    while(True):
        # commitUrl = 'https://api.github.com/repos/'+ USERNAME +'/'+ repo +'/commits?page='+str(pageNo)
        commitUrl = "https://api.github.com/repos/{}/{}/commits?page={}".format(USERNAME, repo, str(pageNo))
        commit_response = requests.get(commitUrl, headers=headers).json()
        sha=[]

        for i in commit_response:
            sha.append((i['sha']))
    # sha="47d192545b617fe187ba0c5aa79f3053928260cb"
        # print(sha)
        for i in sha:
            commitShaUrl="https://api.github.com/repos/{}/{}/commits/{}".format(USERNAME, repo,i)
            currentCommit = {}
            sha_response = requests.get(commitShaUrl, headers=headers).json()
        
            currentCommit['sha']=sha_response['sha']
            currentCommit['date']=sha_response['commit']['committer']['date']
            currentCommit['stats']=sha_response['stats']
    # f=open('test.json')
    # sha_responses=json.load(f)
    # sha_responses{'files'}=[{'filename': 'cpp'},{'filename':'python'}]
    # sha_responses['files'] = 
  
            sha_res_files=[]
            for it in sha_response['files']:
        # currentCommit['files']=it['filename']
                sha_res_files.append(it['filename'])

            currentCommit['files'] = sha_res_files    
            CommDetails.append(currentCommit)
        # CommDetails=[{}]
        # CommDetails[sha].append(sha_response['commit']['committer']['date'])
        # CommDetails[sha].append(sha_response['commit']['author'])
        # CommDetails[sha].append(sha_response['commit']['stats'])
        # CommDetails[sha].append(sha_response['commit']['files']['filename'])

        print(CommDetails)
        break


    #     if(len(watches_response)==0):
    #         break   
    #     pageNo=pageNo+1s
    #     for user in watches_response:
    #         watches.append(user['login'])
    # watches_internal, watches_external = internalExternal(watches, repos)
    # return watches_internal, watches_external
 
def contributionDetails(user,repo,headers):
    contributionDetailUrl = 'https: // api.github.com/repos/USERNAME/REPO/commits'
    pageNo=1
    contributionDetails=[]
    return contributionDetails

# get a repo list of the spesific orgs
def repos(org,headers):
    orgUrl = 'https://api.github.com/orgs/'+org+'/repos'
    repos=[]
    pageNo=1
    while(True):
        repoResponse=requests.get(orgUrl+'?page='+str(pageNo), headers=headers).json()
        if(len(repoResponse)==0):
            break
        pageNo=pageNo+1
        for repo in repoResponse:
            repos.append(repo['name'])
    return repos

# Get list of repos where user is watching
# https://api.github.com/users/USERNAME/subscriptions

def watches(USERNAME,headers,repos):
    watches = []
    pageNo = 1
    while(True):
        watchesUrl = 'https://api.github.com/users/'+USERNAME+'/subscribers?page='+str(pageNo)
        watches_response = requests.get(watchesUrl, headers=headers).json()
        if(len(watches_response)==0):
            break   
        pageNo=pageNo+1
        for repo in watches_response:
            watches.append(repo['name'])
    watches_internal, watches_external = internalExternal(watches, repos)
    return watches_internal, watches_external

# Get list of repos where user is starring
# https://api.github.com/users/USERNAME/starred


# Get list of repos in an org
# https://api.github.com/orgs/ORG/repos

# Filter internal and external repos

# Driver function
def build_for_user(org):
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = helper_methods.getRandomAPIToken(apiDeque)

    # Testing
    users=members(org,headers=headers)
    for user in users:
        print(user)
        userDict={'repos','watches','stars'}
        print(contributing(user,headers=headers))
        userDict.update({'repos': contributing(user, headers=headers)})

        # Read, Extend, Dump to JSON

build_for_user('reddit')



apiDeque=apiRobin.parseConfig('../project.config')
headers=helper_methods.getRandomAPIToken(apiDeque)
coommitDetails('manan-v',headers)
org='reddit'
basememberurl='https://api.github.com/orgs/'+org+'/members'
response=requests.get(basememberurl,headers=headers).json()
for user in response:
    w_internal,w_external=watches(user['login'],headers,repos)
    