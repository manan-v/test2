import requests
import helper_methods
import apiRobin
import json

def topics(repo):
    return repo['topics']

def languages(repo,headers):
    languagesUrl=repo['languages_url']
    languageResponse=requests.get(languagesUrl,headers=headers).json()
    languages=list(languageResponse.keys())
    return languages

def contributors(repo,headers):
    contributorUrl=repo['contributors_url']
    contributors=[]
    pageNo=1
    while(True):
        contributorResponse = requests.get(contributorUrl+'?page='+str(pageNo), headers=headers).json()
        if(len(contributorResponse)==0):
            break
        pageNo=pageNo+1
        for contributor in contributorResponse:
            contributors.append(contributor['login'])
    return contributors

def members(org,headers):
    orgUrl = 'https://api.github.com/orgs/'+org+'/members'
    members=[]
    pageNo=1
    while(True):
        memberResponse=requests.get(orgUrl+'?page='+str(pageNo), headers=headers).json()
        if(len(memberResponse)==0):
            break
        pageNo=pageNo+1
        for member in memberResponse:
            members.append(member['login'])
    return members

def internalExternal(fullList,membersList):
    internal=[]
    external=[]
    for i in fullList:
        if(i not in membersList):
            external.append(i)
        else:
            internal.append(i)
    return internal, external


def watchers(org,repo,headers,members):
    watchers = []
    pageNo = 1
    while(True):
        watcherUrl = 'https://api.github.com/repos/'+org+'/'+repo+'/subscribers?page='+str(pageNo)
        watcher_response = requests.get(watcherUrl, headers=headers).json()
        if(len(watcher_response)==0):
            break   
        pageNo=pageNo+1
        for user in watcher_response:
            watchers.append(user['login'])
    w_internal, w_external = internalExternal(watchers, members)
    return w_internal, w_external

def starrers(org,repo,headers,members):
    starrers = []
    pageNo = 1
    while(True):
        watcherUrl = 'https://api.github.com/repos/'+org+'/'+repo+'/watchers?page='+str(pageNo)
        watcher_response = requests.get(watcherUrl, headers=headers).json()
        if(len(watcher_response)==0):
            break   
        pageNo=pageNo+1
        for user in watcher_response:
            starrers.append(user['login'])
    s_internal, s_external = internalExternal(starrers, members)
    return s_internal, s_external
    
apiDeque=apiRobin.parseConfig('../project.config')
headers=helper_methods.getRandomAPIToken(apiDeque)

org='yeebase'
baseRepoUrl = 'https://api.github.com/orgs/'+org+'/repos'
getRateLimit = 'https://api.github.com/rate_limit'
response=requests.get(baseRepoUrl,headers=headers).json()

for repo in response:
    t=topics(repo)
    l=languages(repo,headers)
    c=contributors(repo,headers)
    m=members(org,headers)
    w_internal,w_external=watchers(org,repo['name'],headers,m)
    s_internal, s_external = starrers(org, repo['name'], headers,m)

    repoDict={}
    repoDict['topics']=t
    repoDict['languages']=l
    repoDict['contributors']=c
    repoDict['watchers_internal']=w_internal
    repoDict['watchers_external'] = w_external
    repoDict['starrers_internal'] = s_internal
    repoDict['starrers_external'] = s_external

    orgDict = json.load(open(org+'.json', 'r'))
    orgDict[repo['name']]=repoDict
    json.dump(orgDict, open(org+'.json','w'))

    print(repo['name'])
    # break
json.dump(orgDict, open(org+'.json', 'a'))
