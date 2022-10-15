import util
import json
import ghMongo

def getLanguageDict(listOfDicts):
    languages=[]
    for dict in listOfDicts:
        tempDict={}
        tempDict.update(
            {'filename': dict['filename'], 'additions': dict['additions'], 'deletions': dict['deletions'], 'changes': dict['changes']})
        languages.append(tempDict)
    return languages

def baseAuthorDict(full_name):
    pageNo=1
    contributorDict = {}

    while(True):
        print(full_name,pageNo)
        response=util.apiRequest('https://api.github.com/repos/'+full_name+'/commits?page='+str(pageNo))
        if(len(response)==0):
            break
        try:
            for commit in response:
                print(full_name, pageNo,commit['sha'], len(response))
                commitDetails=[]
                author=commit['author']['login']
                date=commit['commit']['author']['date']
                sha=commit['sha']
                response = util.apiRequest('https://api.github.com/repos/'+full_name+'/commits/'+sha)
                stats=response['stats']
                # filenames=util.getFieldFromListOfDicts(response['files'],'filename')
                languages=getLanguageDict(response['files'])
                message=commit['commit']['message']
                tempDict={}
                tempDict.update({'sha':sha,'message':message,'date':date,'commitStats':stats,'languages':languages})
                commitDetails.append(tempDict)
                if author not in contributorDict :
                    contributorDict[author]=commitDetails
                else:
                    contributorDict[author].extend(commitDetails)
        except:
            pass
        pageNo=pageNo+1
    return contributorDict

def addUserForRepo(repos):
    for repo in repos:
        print(repo['full_name'])
        if len(repo['contributors']) == 0:
            contributorDict = baseAuthorDict(repo['full_name'])
            repo['contributors'].update(contributorDict)
        break
    return repos

def getReposForOrg(orgName):
    with open('baseDict/'+orgName+'.json','r') as f:
        oldRepos=json.load(f)
    newRepos=addUserForRepo(oldRepos)
    with open('repoUserDict/'+orgName+'.json', 'w') as f:
        json.dump(newRepos,f)

# mydb=ghMongo.connect('repoStruct')
# getReposForOrg('10gen')
# json.dump(baseAuthorDict('10gen/envoy-serverless'),open('apiTester.json','w'))