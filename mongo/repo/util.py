import requests 
import json
import sys
import os
sys.path.append('../../step1_obtainRepoDetails')
sys.path.append('../../extra/misc')
from helper_methods import getRandomAPIToken
import apiRobin

def apiRequest(reqUrl):
    apiDeque = apiRobin.parseConfig('../../project.config')
    headers = getRandomAPIToken(apiDeque)
    print(headers)
    response = requests.get(reqUrl,
                            headers=headers).json()
    json.dump(response,open('apiTester_reverse.json','w'))
    return response

def reqURLReturnDict(reqUrl, keyOfListOfDict):
    apiDeque = apiRobin.parseConfig('../../project.config')
    headers = getRandomAPIToken(apiDeque)

    response = requests.get(reqUrl,
                            headers=headers).json()
    if (response[keyOfListOfDict]):
        return response[keyOfListOfDict]
    else:
        raise Exception("Invalid key - not found!")

def getFieldFromListOfDicts(listOfDicts, field):
    fieldList=[]
    for dict in listOfDicts: 
        fieldList.append(dict[field])
    return fieldList


# dict=reqURLReturnDict(
#     'https://api.github.com/repos/10gen/envoy-serverless/commits','commit')

# with open('utilTest.json','w') as f:
#     json.dump(dict,f)

# print(type(listOfDicts))
# fieldList=getFieldFromListOfDicts(json.load(open('utilTest.json','r')),'filename')
# print(fieldList)