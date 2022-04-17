import sys
import requests, json, argparse
import apiRobin
from time import sleep
from tqdm import tqdm
from helper_methods import *
# Sample: python3 getGithubOrgDetails.py --config_file project.config --min_val 1 --max_val 10000 --output_file githubOrgDetails.txt
# Alternate: python3 getGithubOrgDetails.py --min_val 12327 --max_val 12333 --output_file githubOrgDetails.txt
# Args to run the code
parser = argparse.ArgumentParser()
parser.add_argument('--config_file')
parser.add_argument('--min_val')
parser.add_argument('--max_val')
parser.add_argument('--output_file')

args = vars(parser.parse_args())
apiDeque=apiRobin.parseConfig(args['config_file'])

def getGithubOrgDetails(idVal, headers):
	response = requests.get(reqUrl + str(idVal), headers=headers).json()
	if 'message' not in response:
		return response
	else:
		return None

headers = getAPIToken(apiDeque)		

# Get organization data and GitHub request header
reqUrl = "https://api.github.com/organizations/"


with open(args['output_file'], 'a') as outfile:

	# GitHub orgs are stored with IDs from (1-n)
	for orgId in tqdm(range(int(args['min_val']), int(args['max_val']))):
		while True:
			try:
				# Get JSON response from GitHub
				response = getGithubOrgDetails(orgId, headers)

				# If org exists then write to file (newline separated)
				if response:
					json.dump(response, outfile)
					outfile.write('\n')
				break # If no exception occurred
			# Need to replace with the exact rate limit exception
			except Exception as e:
				if e.code == 403:
					print("** SWITCHING TOKEN NOW **")
					headers = getAPIToken(apiDeque)
				else:
					print("** SLEEPING FOR 1 HR **")
					sleep(3600)