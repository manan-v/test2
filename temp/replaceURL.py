from ast import Pass
import requests
import json
import argparse
from time import sleep
from tqdm import tqdm
# from helper_methods import *

#  TODO: Write script to update links in parent.json with the response for each URL
#  FIXME: Replace value in the response dict
#  NOTE: Consider the json as dict - and not a json
# def updateData(key, newValue, parent, child):
#     for key, value in parent.items():
#         if key==


def replaceURL(parentJSON, childJSON):
    counter = 1
    totCounter = 1
    excludeUrl = ['avatar', 'html']
    with open(parentJSON, 'r+') as parent:
        parentContent = json.loads(parent.read())
        for urlField, reqUrl in parentContent.items():
            if "url" in urlField and not any(exclude in urlField for exclude in excludeUrl) and len(urlField) > 3:
                print(urlField+" - "+reqUrl)
        # response = requests.get(reqUrl, headers=headers).json()
        # FIXME - replace harcoded response with requested response
    keyToBeReplaced='repos_url'
    with open(childJSON, 'r+') as child:
        response = json.loads(child.read())
    for key, value in parentContent.items():
        if key==keyToBeReplaced:
            parentContent[key]=response
            with open(parentJSON, 'w+') as parent:
                parentContent=json.dumps(parentContent)
                parent.write(parentContent)
                # print(parentContent[keyToBeReplaced])

            # Pass
    # print(parentContent[keyToBeReplaced])
        


        # with open('test2.json', 'a') as outfile:
        #     if 'message' not in response and response is not None:
        #         json.dump(response, outfile)
        #         print("counter is:"+str(counter))
        #         counter+=1
        #         print("You made it "+urlField)


replaceURL("D:\Code\github-recommendation-project\json\parent.json",
           "D:\Code\github-recommendation-project\json\child.json")
