import requests
import json
import argparse
import apiRobin
from time import sleep
from tqdm import tqdm
# import getGithubOrgDetails

# Sample: python3 getSpecificOrgDetails.py --config_file project.config --org_name novelys --output_file githubSpecificOrgDetails.json
reqUrl = "https://api.github.com/orgs/"

parser = argparse.ArgumentParser()
parser.add_argument('--config_file')
parser.add_argument('--org_name')
parser.add_argument('--output_file')

args = vars(parser.parse_args())

apiDeque = apiRobin.parseConfig(args['config_file'])


def getAPIToken(apiDeque):
    # Rotate the API queue
    apiDeque = apiRobin.rotateAPI(apiDeque)

    # Create the new header
    headers_new = {'Authorization': 'token ' + apiDeque[0]}
    print(" ** TOKEN SELECTED: {} **".format(headers_new))
    return headers_new


def getSpecificOrgDetails(orgName, headers):
    response = requests.get(reqUrl + str(orgName), headers=headers).json()
    if 'message' not in response:
        return response
    else:
        return None


def replaceURL(response):
    with open(response, 'r+') as file:
        content = json.loads(file.read())
        for urlField,reqUrl in content.items():
            if "url" in urlField and len(urlField) > 3:
                print(urlField, reqUrl)
    # urlResponse=requests.get(reqUrl,str('novelys'), headers=headers)
    # content.replace(,)


headers = getAPIToken(apiDeque)

with open(args['output_file'], 'a') as outfile:
    # GitHub orgs are stored with IDs from (1-n)
    while True:
        try:
            # Get JSON response from GitHub
            response = getSpecificOrgDetails(args['org_name'], headers)

            # If org exists then write to file (newline separated)
            if response:
                json.dump(response, outfile)
                outfile.write('\n')
            break  # If no exception occurred
        # Need to replace with the exact rate limit exception
        except Exception as e:
            if e.code == 403:
                print("** SWITCHING TOKEN NOW **")
                headers = getAPIToken(apiDeque)
            else:
                print("** SLEEPING FOR 1 HR **")
                sleep(3600)

replaceURL("test.json")
