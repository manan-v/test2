from operator import or_
import requests
import json
import argparse
from time import sleep
from tqdm import tqdm
from helper_methods import *

# Sample: python3 getSpecificOrgDetails.py --config_file project.config --org_name novelys --output_file githubSpecificOrgDetails.json
reqUrl = "https://api.github.com/orgs/"

# Parse the arguements
parser = argparse.ArgumentParser()
parser.add_argument('--config_file')
parser.add_argument('--org_name')
parser.add_argument('--output_file')
args = vars(parser.parse_args())

# Get the API key to use
apiDeque = apiRobin.parseConfig(args['config_file'])
headers = getAPIToken(apiDeque)

# Request an organisation name and return the response
def getSpecificOrgDetails(orgName, headers):
    response = requests.get(reqUrl + str(orgName), headers=headers).json()
    if 'message' not in response:
        return response
    else:
        return None

# Get the JSON file with URLs
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
        # Switch token when limit exhausted
        except Exception as e:
            if e.code == 403:
                print("** SWITCHING TOKEN NOW **")
                headers = getAPIToken(apiDeque)
            else:
                print("** SLEEPING FOR 1 HR **")
                sleep(3600)

# Request each URL and return responses as list
def getResponseFromURL(parentJSON, excludeUrl):
    # Initialise empty lists to store keys, oldValue and newValue
    keyToBeReplaced=[]
    oldValue=[]
    newValue = []
    with open(parentJSON, 'r+') as parent:
        parentContent=json.loads(parent.read())
        # Gets the list of keys and old values
        for key, value in parentContent.items():
            # Append only if the key is absent in excludeUrl list
            if "url" in key and not any(exclude in key for exclude in excludeUrl):
                keyToBeReplaced.append(key)
                oldValue.append(value)
                # TODO Add try except statement to switch API post exhaustion
                response = requests.get(value, headers=headers).json()
                newValue.append(response)
            
        # Organisation's URL (for eg: https://api.github.com/orgs/novelys) is not useful
        keyToBeReplaced.pop(0)
        oldValue.pop(0)
        newValue.pop(0)
    
    return keyToBeReplaced, oldValue, newValue

# Define keys that are to be excluded while search
excludeUrl = ['avatar', 'html', 'members']
# Get the keys, oldValues and newValues
keyToBeReplaced, oldValue, newValue=getResponseFromURL(args['output_file'],excludeUrl)

with open(args['output_file']) as parent:
    parentContent = json.loads(parent.read())
    iterator=0
    # Iterate over the entire file
    for key, value in parentContent.items():
        # If a key is found in the keyToBeReplaced list
        if(key == keyToBeReplaced[iterator]):
            # Replace the current value with the corresponding response from newValue 
            parentContent[key]=newValue[iterator]
            iterator=iterator+1
            # Prevents index out of bounds error
            if(iterator==len(keyToBeReplaced)):
                break
with open(args['output_file'],'w+') as parent: 
    # Rewrite the JSON with the updated data
    parentContent=json.dumps(parentContent)
    parent.write(parentContent)
print(" ** URLs REPLACED FOR ORG '"+args['org_name']+"' IN FILE : '"+args['output_file']+"' **")