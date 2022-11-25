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
    commitsDet = []
    pageNo = 1
    repo =''

    while(True):
        commitUrl = 'https://api.github.com/repos/'+ USERNAME +'/'+ repo +'/commits?page='+str(pageNo)
        commit_response = requests.get(commitUrl, headers=headers).json()
        sha=[]
        
        for sha in commit_reposonse:
            sha.append(commit_response['sha'])
        
        commitShaUrl='https://api.github.com/repos/'+ USERNAME +'/'+ repo +'/commits'+sha
        sha_response = requests.get(commitShaUrl, headers=headers).json()
        CommDetails=[[]]
        CommDetails[0].append(sha_response['commit']['committer'])
        CommDetails[0].append(sha_response['commit']['author'])
        CommDetails[0].append(sha_response['commit']['stats'])
        CommDetails[0].append(sha_response['commit']['files']['filename'])

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

# Get list of repos where user is watching
# https://api.github.com/users/USERNAME/subscriptions

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
