import pymongo
def checkIfContributorsEmpty(orgName,full_name):
    cluster = pymongo.MongoClient(
        "mongodb+srv://superman:mongo123@cluster0.4soxef8.mongodb.net/test")
    db=cluster['repoStruct']
    collection=db[orgName]

    results = collection.find_one({'full_name': full_name})
    # print(len(results['contributors']))
    if(len(results['contributors'])==0):
        return True
    else:
        return False

# print(checkIfContributorsEmpty('99designs','99designs/alchemy_cms'))