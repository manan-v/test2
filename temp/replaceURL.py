import requests
import json
import argparse
from time import sleep
from tqdm import tqdm
# from helper_methods import *

reqUrl = "https://api.github.com/orgs/"

# parser = argparse.ArgumentParser()
# parser.add_argument('--config_file')
# parser.add_argument('--org_name')
# parser.add_argument('--output_file')
# args = vars(parser.parse_args())

# apiDeque = apiRobin.parseConfig(args['config_file'])
apiDeque = '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'
headers = apiDeque


def replaceURL(parentJSON):
    # counter = 1
    # totCounter = 1
    # List of fields that should be excluded
    iterator=0
    excludeUrl = ['avatar', 'html']
    # List of fields that should be included
    keyToBeReplaced = []
    oldValue=[]
    # Iterate through the mainURL and extract fields to replace
    with open(parentJSON, 'r+') as parent:
        parentContent = json.loads(parent.read())
        # Gets the list of keys and old values
        for urlField, reqUrl in parentContent.items():
            if "url" in urlField and not any(exclude in urlField for exclude in excludeUrl) and len(urlField) > 3:
                print(urlField+" - "+reqUrl)
                keyToBeReplaced.append(urlField)
                oldValue.append(reqUrl)
        # Gets the new value
        newValue=[]
        for key in keyToBeReplaced:
            iterator=0

            headerInfo = {'content-type': 'application/json;charset=UTF-8'}
            response = requests.get(oldValue[iterator], headers=headers).json()
            # print(response)
            newValue.append(response)
            iterator+=1
        print("I have "+str(len(newValue))+" new values and "+str(len(keyToBeReplaced))+" keys.")
        print(newValue[5])
        if key == keyToBeReplaced[0]:
            parentContent[key] = newValue[0]
            with open(parentJSON, 'w+') as parent:
                parentContent = json.dumps(parentContent)
                parent.write(parentContent)
        # Iterate over the mainJSON - and replace old with new
        # for key, value in parentContent.items():
        #     # iterator=0
        #     # if key==keyToBeReplaced[iterator]:
        #     if key == keyToBeReplaced[0]:
        #         parentContent[key] = newValue[0]
        #         with open(parentJSON, 'w+') as parent:
        #             parentContent = json.dumps(parentContent)
        #             parent.write(parentContent)
        # FIXME - replace harcoded response with requested response
    # keyToBeReplaced = 'repos_url'

    # with open(childJSON, 'r+') as child:
    #     response = json.loads(child.read())
    # for key, value in parentContent.items():
    #     if key == keyToBeReplaced[0]:
    #         parentContent[key] = response
    #         with open(parentJSON, 'w+') as parent:
    #             parentContent = json.dumps(parentContent)
    #             parent.write(parentContent)
                # print(parentContent[keyToBeReplaced])

            # Pass
    # print(parentContent[keyToBeReplaced])

        
        # with open('test2.json', 'a') as outfile:
        #     if 'message' not in response and response is not None:
        #         json.dump(response, outfile)
        #         print("counter is:"+str(counter))
        #         counter+=1
        #         print("You made it "+urlField)
replaceURL("parent.json")
