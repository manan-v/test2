import requests
import json
import apiRobin
import helper_methods

def repo(user,header):
    repoUrl = 'https://api.github.com/orgs/'+org+'/members'

apiDeque = apiRobin.parseConfig('../project.config')
headers = helper_methods.getRandomAPIToken(apiDeque)

org='reddit'
baseUserUrl='https://api.github.com/orgs/'+org+'/members'
getRateLimit = 'https://api.github.com/rate_limit'
response = requests.get(baseUserUrl, headers=headers).json()

for user in response:
    print(user['login'])