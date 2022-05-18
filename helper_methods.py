import apiRobin
import json

def getAPIToken(apiDeque):
    # Rotate the API queue
    apiDeque = apiRobin.rotateAPI(apiDeque)

    # Create the new header
    headers_new = {'Authorization': 'token ' + apiDeque[0]}
    print(" ** TOKEN SELECTED: {} **".format(headers_new))
    return headers_new

def getRandomAPIToken(apiDeque):
    # Rotate the API queue
    apiDeque = apiRobin.randomRotateAPI(apiDeque)

    # Create the new header
    headers_new = {'Authorization': 'token ' + apiDeque[0]}
    # print(" ** TOKEN SELECTED: {} **".format(headers_new))
    return headers_new


def replaceURL(parentJSON, childJSON):
    # counter = 1
    # totCounter = 1
    excludeUrl = ['avatar', 'html']
    keyToBeReplaced=[]
    with open(parentJSON, 'r+') as parent:
        parentContent = json.loads(parent.read())
        for urlField, reqUrl in parentContent.items():
            if "url" in urlField and not any(exclude in urlField for exclude in excludeUrl) and len(urlField) > 3:
                print(urlField+" - "+reqUrl)
                keyToBeReplaced.append(urlField)
        # response = requests.get(reqUrl, headers=headers).json()
        # FIXME - replace harcoded response with requested response
    # keyToBeReplaced = 'repos_url'
    with open(childJSON, 'r+') as child:
        response = json.loads(child.read())
    for key, value in parentContent.items():
        if key == keyToBeReplaced[1]:
            parentContent[key] = response
            with open(parentJSON, 'w+') as parent:
                parentContent = json.dumps(parentContent)
                parent.write(parentContent)
                # print(parentContent[keyToBeReplaced])

            # Pass
    # print(parentContent[keyToBeReplaced])
