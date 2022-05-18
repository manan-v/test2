from helper_methods import * 
import time, math

# NOTE: To run the code - delete getSpecificOrgDetailsData/novelys.json if already present
# Sample: python3 getSpecificOrgDetails-helper.py 

start=time.time()

with open('top-repo') as orgs:
    for line in orgs:
        orgName, number = line.strip().split(None, 1)
        replaceURL(orgName,'project.config','getSpecificOrgDetailsData/'+orgName+'.json')

end=time.time()

print(" ** THE EXECUTION TOOK: "+str(math.floor(end-start))+" SECONDS **")
