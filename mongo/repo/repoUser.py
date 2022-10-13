import util
import json

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
        response=util.apiRequest('https://api.github.com/repos/'+full_name+'/commits?page='+str(pageNo))
        if(len(response)==0):
            break
        try:
            for commit in response:
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

# contributorDict=baseAuthorDict('10gen/mongo-orchestration')
# json.dump(contributorDict,open('repoUser.json','w'))

with open('../10gen.json','r') as f:
    repos=json.load(f)
for repo in repos:
    print(repo['full_name'])
    if len(repo['contributors'])==0:
        contributorDict=baseAuthorDict(repo['full_name'])
        repo['contributors'].update(contributorDict)
    # break
with open('../10gen.json', 'w') as f:
    json.dump(repos,f)