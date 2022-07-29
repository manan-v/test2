import sys
import requests
import json
import argparse
import os

# Sample: python3 getGithubRepoDetails.py --api_key "token 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" --repoDir repoDir
# Args to run the code
parser = argparse.ArgumentParser()
parser.add_argument('--api_key')
parser.add_argument('--organization_file')
parser.add_argument('--repoDir')

args = vars(parser.parse_args())

# Create directory if not exists
if not os.path.exists('repoDir'):
    os.makedirs('repoDir')

# GitHub request header
headers = {'Authorization':  args['api_key']}

with open(args['organization_file'], 'r') as fr:
	content = fr.read().split('\n')

def getRepoDetails(reqURL):
	response = requests.get(reqURL).json()
	if 'message' not in response:
		return response

for vals in content:
	try:
		# Get organization details
		organization = json.loads(vals)

		# Get repo details 
		response = getRepoDetails(organization["repos_url"])

		# Write repo details to file
		with open(os.path.join(args['repoDir'],organization["login"] + '.json'), 'w') as f:
			json.dump(response, f)

	except json.decoder.JSONDecodeError:
		pass