import pymongo

def connect():
  myclient = pymongo.MongoClient(
      "mongodb+srv://superman:mongo123@cluster0.4soxef8.mongodb.net/test")
  dblist = myclient.list_database_names()
  print(dblist)
  if "github" in dblist:
    print("The database exists.")
  mydb=myclient['github']
  return mydb

def dataToPush(mydb, mydict,tableName="repo"):
  # mydict = [{ "name": "John", "address": "Highway 37" }]
  mycol = mydb[tableName]
  x = mycol.insert_many(mydict)

def connectAndPush(dataDict):
  mydb=connect()
  dataToPush(mydb,dataDict)
