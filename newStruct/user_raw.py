import requests
import json
import apiRobin
import helper_methods

# Get list of repos where user contributes
# https://api.github.com/users/USERNAME/repos
def contributing(user,headers):
    contributingUrl='https://api.github.com/users/'+user+'/repos'
    pageNo=1
    while(True):
        contributionResponse=requests.get(contributingUrl+'?page='+str(pageNo),headers=headers).json()
        if(len(contributionResponse)==0):
            break
        for contribution in contributionResponse:
            print(contribution['name'])
        pageNo+=1

# Get further details for contributions
    # https://api.github.com/repos/USERNAME/REPO/commits , get `sha`
    # -> https://api.github.com/repos/USERNAME/REPO/commits/SHA, 
    # get `sha`
    # get `committer.author.date`
    # get `stats`
    # get `file['filename'] for file in files` 

# Get list of repos where user is watching
# https://api.github.com/users/USERNAME/subscriptions

# Get list of repos where user is starring
# https://api.github.com/users/USERNAME/starred


# Get list of repos in an org
# https://api.github.com/orgs/ORG/repos

# Filter internal and external repos

# Driver function
def build_for_user(user):
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = helper_methods.getRandomAPIToken(apiDeque)

    # Testing
    contributing(user,headers=headers)

build_for_user('c9s')
