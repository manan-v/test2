import apiRobin

def getAPIToken(apiDeque):
    # Rotate the API queue
    apiDeque = apiRobin.rotateAPI(apiDeque)

    # Create the new header
    # headers_new = {'Authorization': 'token ' + apiDeque[0]}
    print(" ** TOKEN SELECTED: {} **".format(headers_new))
    return headers_new

def getRandomAPIToken(apiDeque):
    # Rotate the API queue
    apiDeque = apiRobin.randomRotateAPI(apiDeque)

    # Create the new header
    headers_new = {'Authorization': 'token ' + apiDeque[0]}
    # print(" ** TOKEN SELECTED: {} **".format(headers_new))
    return headers_new