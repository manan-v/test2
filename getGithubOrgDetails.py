import sys
import requests
import json
import argparse
import apiRobin

# Sample: python3 getGithubOrgDetails.py --api_key "token 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" --min_val 12327 --max_val 12333 --output_file githubOrgDetails.txt
# Alternate: python3 getGithubOrgDetails.py --min_val 12327 --max_val 12333 --output_file githubOrgDetails.txt

# Args to run the code
parser = argparse.ArgumentParser()
# parser.add_argument('--api_key')
parser.add_argument('--min_val')
parser.add_argument('--max_val')
parser.add_argument('--output_file')

args = vars(parser.parse_args())
apiDeque=apiRobin.parseConfig('project.config')

# Get organization data
reqUrl = "https://api.github.com/organizations/"


def getGithubOrgDetails(idVal):
	response = requests.get(reqUrl + str(idVal), headers=headers).json()
	if 'message' not in response:
		return response
	else:
		return None


for i in range(20):
	# GitHub request header
	apiDeque = apiRobin.rotateAPI(apiDeque)
	headers = {'Authorization': 'token '+apiDeque[0]}
	print(headers)

	with open(args['output_file'], 'a') as outfile:
		# GitHub orgs are stored with IDs from (1-n)
		for orgId in range(int(args['min_val']), int(args['max_val'])):
			# Get JSON response from GitHub
			response = getGithubOrgDetails(orgId)

			# If org exists then write to file (newline separated)
			if response:
				json.dump(response, outfile)
				outfile.write('\n')
