import sys
import requests, json, argparse
import apiRobin
from time import sleep
from tqdm import tqdm
from helper_methods import *
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm
import json
import os

num_cores = multiprocessing.cpu_count()
print('Total number of cores: {}'.format(num_cores))

# Sample: python3 getGithubOrgDetails.py --config_file project.config --min_val 1 --max_val 10000 --output_file githubOrgDetails.txt
# Alternate: python3 getGithubOrgDetails.py --min_val 12327 --max_val 12333 --output_file githubOrgDetails.txt
# Args to run the code
parser = argparse.ArgumentParser()
parser.add_argument('--config_file')
# parser.add_argument('--min_val')
# parser.add_argument('--max_val')
# parser.add_argument('--output_file')
# parser.add_argument('--orgName')

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

# Get repo details
def getRepoDetails(orgName):
	orgDetails = {}

	pageCounter = 0
	memberDetails = []

	# Get member details
	while True:
		try:
			reqUrl = "https://api.github.com/orgs/" + orgName + "/members?page=" + str(pageCounter)
			headers = getRandomAPIToken(apiDeque)
			member_response = requests.get(reqUrl, headers=headers).json()

			memberDetails.extend(member_response)
			pageCounter += 1

			# If response is []
			if len(member_response) == 0:
				break
		except:
			break

	orgDetails['memberDetails'] = memberDetails

	pageCounter = 0
	repoDetails = []

	while True:
		# response - repo details with url
		reqUrl = "https://api.github.com/orgs/" + orgName + "/repos?page=" + str(pageCounter)
		headers = getRandomAPIToken(apiDeque)
		response = requests.get(reqUrl, headers=headers).json()

		repo_counter = 0
		try:
			# Get contributors
			for repo in response:
				contributors_pagecounter = 0 
				contributors_list = []
				while True:
					# print(f"Repo : {repo['name']}, Contributor Page: {contributors_pagecounter}")
					reqUrl = "https://api.github.com/repos/" + orgName + "/" + repo['name'] + "/contributors?page=" + str(contributors_pagecounter)
					headers = getRandomAPIToken(apiDeque)
					contributors = requests.get(reqUrl, headers=headers).json()
					contributors_list.extend(contributors)

					if len(contributors) == 0:
						break

					contributors_pagecounter += 1
				response[repo_counter]['contributors'] = contributors_list
				repo_counter += 1
			repoDetails.extend(response)
		except:
			pass
		pageCounter += 1

		# If response is []
		if len(response) == 0:
			break

	orgDetails['repoDetails'] = repoDetails
	return orgDetails

# Get organization data and GitHub request header
# reqUrl = "https://api.github.com/organizations/"

# value_range = list(range(int(args['min_val']), int(args['max_val'])))
# processed_list = Parallel(n_jobs=num_cores)(delayed(getGithubOrgDetails)(i) for i in tqdm(value_range))

# Get member details and repo details from organization name
# print("** Getting member details **")
# member_details = getMemberDetails(args['orgName'])
# print("** Getting repo details **")

# ******************
alreadyDone = os.listdir('repo_details')

with open("githubOrgDetails.txt","r") as fr:
	content = fr.read().split('\n')
	orgName = []
	for org in content:
		try:
			orgName.append(json.loads(org)['login'])
		except:
			pass

for name in tqdm(orgName):
	if name + ".json" in alreadyDone:
		print(f"Done: {name}")
		continue
	
	print(f"Get repo details: {name}")
	repo_details = getRepoDetails(name)

	# Get contributors for repos
	with open("repo_details/" + name + ".json", "w") as outfile:
		outfile.write(json.dumps(repo_details))