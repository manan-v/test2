import configparser
from collections import deque


def getAPI():
    # Parse through the config file
    parser = configparser.ConfigParser()
    parser.read('project.config')

    # Extract allAPI as string, convert to deque
    for sect in parser.sections():
        for name, value in parser.items(sect):
            allAPI = value
    allAPI = allAPI.strip("[]")
    apiSeperated = deque(allAPI.split(","))
    print(apiSeperated[0])
    print(len(apiSeperated))

    # return
getAPI()
