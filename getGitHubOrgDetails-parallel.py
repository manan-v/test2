import sys
import requests, json, argparse
import apiRobin
from time import sleep
from tqdm import tqdm
from helper_methods import *
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm

num_cores = multiprocessing.cpu_count()
print('Total number of cores: {}'.format(num_cores))

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

# Get ID of GitHub organization
def getGithubOrgDetails(idVal):
	while True:
		headers = getRandomAPIToken(apiDeque)
		try:
			response = requests.get(reqUrl + str(idVal), headers=headers).json()
			if 'message' not in response:
				with open(args['output_file'], 'a') as outfile:
					json.dump(response, outfile)
					outfile.write('\n')
			break
		except ConnectionResetError:
			print("** SWITCHING TOKEN NOW **")
			newAPIToken = getRandomAPIToken(apiDeque)
			if newAPIToken != headers:
				headers = getAPIToken(apiDeque)
		except Exception as e:
			print("** SLEEPING FOR 1 HR **")
			sleep(3600)

# Get member details
def getMemberDetails(orgName):
	pageCounter = 0
	memberDetails = []

	while pageCounter < 100:
		reqUrl = "https://api.github.com/orgs/" + orgName + "/members?page=" + str(pageCounter)
		headers = getRandomAPIToken(apiDeque)
		response = requests.get(reqUrl, headers=headers).json()

		memberDetails.extend(response)
		pageCounter += 1

		# If response is []
		if len(response) == 0:
			break

	return memberDetails

# Get repo details
def getRepoDetails(orgName):
	pageCounter = 0
	repoDetails = []

	while pageCounter < 100:
		reqUrl = "https://api.github.com/orgs/" + orgName + "/repos?page=" + str(pageCounter)
		headers = getRandomAPIToken(apiDeque)
		response = requests.get(reqUrl, headers=headers).json()

		repoDetails.extend(response)
		pageCounter += 1

		# If response is []
		if len(response) == 0:
			break

	return repoDetails
# Get organization data and GitHub request header
# reqUrl = "https://api.github.com/organizations/"

# value_range = list(range(int(args['min_val']), int(args['max_val'])))
# processed_list = Parallel(n_jobs=num_cores)(delayed(getGithubOrgDetails)(i) for i in tqdm(value_range))
# getMemberDetails("LCS2-IIITD")
print(getRepoDetails("LCS2-IIITD"))