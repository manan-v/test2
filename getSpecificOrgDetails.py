import requests, json, argparse
import apiRobin
from time import sleep
from tqdm import tqdm
# import getGithubOrgDetails

# Sample: python3 getSpecificOrgDetails.py --config_file project.config --org_name novelys --output_file githubOrgDetails.txt
reqUrl = "https://api.github.com/orgs/"

parser = argparse.ArgumentParser()
parser.add_argument('--config_file')
parser.add_argument('--org_name')
parser.add_argument('--output_file')

args = vars(parser.parse_args())

apiDeque=apiRobin.parseConfig(args['config_file'])

def getSpecificOrgDetails(orgName, headers):
    response = requests.get(reqUrl + str(orgName), headers=headers).json()
    if 'message' not in response:
            return response
    else:
        return None

def getAPIToken(apiDeque):
	# Rotate the API queue
	apiDeque = apiRobin.rotateAPI(apiDeque)

	# Create the new header
	headers_new = {'Authorization': 'token ' + apiDeque[0]}
	print(" ** TOKEN SELECTED: {} **".format(headers_new))
	return headers_new

headers = getAPIToken(apiDeque)

print(getSpecificOrgDetails(args['org_name'],headers))