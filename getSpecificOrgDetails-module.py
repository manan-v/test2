from getSpecificOrgDetails import *
import time, math

# NOTE: To run the code - delete getSpecificOrgDetailsData/novelys.json if already present
#       else: You may recieve 'json.decoder.JSONDecodeError: Extra data:' error
# Also, make sure there is a directory named getSpecificOrgDetailsData on the same level
# Sample: python3 getSpecificOrgDetails-module.py 

start=time.time()

with open('top-repo') as orgs:
    for line in orgs:
        orgName, number = line.strip().split(None, 1)
        replaceURL(orgName, 'project.config',
                              'getSpecificOrgDetailsData/'+orgName+'.json')
        # Uncomment the break if you want to run it only once
        # break
end=time.time()

print(" ** THE EXECUTION TOOK: "+str(math.floor(end-start))+" SECONDS **")