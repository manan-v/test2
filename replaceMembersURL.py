import re
from tabnanny import check
from webbrowser import get
import requests
import json
import argparse
from time import sleep
from helper_methods import *

# NOTE: To run the code - delete getSpecificOrgDetailsData/novelys.json if already present
# Sample: python3 replaceMembersURL.py --config_file project.config --org_name GITenberg

# Parse the arguements
parser = argparse.ArgumentParser()
parser.add_argument('--config_file')
parser.add_argument('--org_name')
parser.add_argument('--output_file')
args = vars(parser.parse_args())

def replaceMembersURL(orgName,configFile):
    membersReqURL = "https://api.github.com/orgs/" +orgName+"/members?page="

    # Get the API key to use
    apiDeque = apiRobin.parseConfig(configFile)
    print(" ** THE TOKEN BELOW IS FOR MEMBERS_URL ** ")
    headers = getAPIToken(apiDeque)

    # Start from this page
    pageNumber = 1
    # Empty list initialised to store responses from members URL
    memberValue = []

    # Request an organisation name and return the response
    def checkIfListNotEmpty(response):
        # returns true for an empty list
        if not response:
            return True
        # and false for a non-empty list
        else:
            return False

    # Get response from a particular members page
    def getResponse(membersReqURL, pageNumber):
        membersReqURL = membersReqURL+str(pageNumber)
        response = requests.get(membersReqURL, headers=headers).json()
        return response

    while(True):
        response = getResponse(membersReqURL, pageNumber)
        # Check for list contents - and break if list is empty
        if(checkIfListNotEmpty(response)):
            break
        else:
            memberValue.extend(response)
            pageNumber += 1
            # sleep(0.01)

    # with open('membersURLData/'+orgName+'.json', 'a') as outfile:
    #     json.dump(memberValue, outfile)
    #     outfile.write('\n')
    return memberValue

# memberValue=replaceMembersURL(args['org_name'],args['config_file'])
# print(memberValue)