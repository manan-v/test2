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

def getGithubOrgDetails(idVal):
	headers = getAPIToken(apiDeque)	
	try:
		response = requests.get(reqUrl + str(idVal), headers=headers).json()
		if 'message' not in response:
			with open(args['output_file'], 'a') as outfile:
				json.dump(response, outfile)
				outfile.write('\n')
	except Exception as e:
		if e.message == "Connection reset by peer":
			print("** SWITCHING TOKEN NOW **")
			headers = getAPIToken(apiDeque)
		else:
			print("** SLEEPING FOR 1 HR **")
			sleep(3600)

	

# Get organization data and GitHub request header
reqUrl = "https://api.github.com/organizations/"

value_range = list(range(int(args['min_val']), int(args['max_val'])))
processed_list = Parallel(n_jobs=num_cores)(delayed(getGithubOrgDetails)(i) for i in tqdm(value_range))