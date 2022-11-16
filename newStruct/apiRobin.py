import configparser
from collections import deque
import random

def parseConfig(pathToConfig):
    # Parse through the config file
    parser = configparser.ConfigParser()
    parser.read(pathToConfig)
    # Extract allAPI as string, convert to deque
    for sect in parser.sections():
        for name, value in parser.items(sect):
            allAPI = value
    allAPI = allAPI.strip("[]")
    apiDeque = deque(allAPI.split(","))
    return apiDeque

def noOfTokens():
    return len(parseConfig())

def rotateAPI(apiDeque):
    apiDeque.rotate()
    return apiDeque

def randomRotateAPI(apiDeque):
    random.shuffle(apiDeque)
    return apiDeque
