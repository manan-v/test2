import pymongo

def connect(dbName):
  myclient = pymongo.MongoClient(
      "mongodb+srv://superman:mongo123@cluster0.4soxef8.mongodb.net/test")
  dblist = myclient.list_database_names()
  print(dblist)
  if dbName in dblist:
    print("The database exists.")
  mydb = myclient[dbName]
  return mydb

def dataToPush(mydb, mydict,tableName="repo"):
  # mydict = [{ "name": "John", "address": "Highway 37" }]
  mycol = mydb[tableName]
  x = mycol.insert_many(mydict)

def connectAndPush(dataDict,orgName, dbName):
  mydb=connect(dbName)
  dataToPush(mydb,dataDict,orgName)

def updateUserForRepo(dbName,orgName,repo,dataDict):
  mycol=dbName[orgName]
  
