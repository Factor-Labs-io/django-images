import os
from dotenv import load_dotenv
load_dotenv() 
# from myClasses import UserObj, ActivePool
import pymongo
from . import database

url = os.environ.get("MONGODB_URL")  

obj_created = 1
obj_begin_postgre_update = 4
obj_currently_being_processed = 5
obj_completed_postgre_update = 6

# Connect to MongoDB
client = pymongo.MongoClient(url)
print(client)

# Select a database
db = client.myDatabase

# Select a collection
mycollection = db["active_pool"]

def enter_MongoDb_data():
    try:
        # Define a doc to insert into the collection
        result = database.dbQueryAll()

        # Insert each item in the dictionary with a unique ID
        for result, value in result.items():
#             print(value['token_id'])

            # Stores the data as is
            mycollection.insert_one(value)
            mycollection.update_one({"_id": value["_id"]},{"$set": {"state": obj_created}})
    except Exception as e:
        print("Mongodb error: ", e)

def destroy_MongoDB():
    try:
        results = mycollection.find()
        data = []

        if results is not None:
            for doc in results:
                mycollection.update_one({"_id": doc["_id"]},{"$set": {"state": obj_begin_postgre_update}})
                entry = {
                "token_id": str(doc["token_id"]),
                "twitter_id": doc["twitter_id"],
                "address": doc["address"],
                "pfp_status": doc["pfp_status"],
                "points": str(doc["points"])
            }
                data.append(entry)
                if doc['pfp_status'] == True:
                    entry['points'] = int(entry['points']) + 1
                if doc['pfp_status'] == False:
                    entry['pfp_status'] = False
                mycollection.update_one({"_id": doc["_id"]},{"$set": {"state": obj_currently_being_processed}})

                # Update postgresql with the data stored in the dictionary
                database.dbUpdatePostgre(entry['address'], entry['twitter_id'], entry['token_id'] , entry['pfp_status'], entry['points'])
                mycollection.update_one({"token_id": doc["token_id"]},{"$set": {"state": obj_completed_postgre_update}})
            delete_result = mycollection.delete_many({})
            print(delete_result.deleted_count, " documents deleted.")

#             print(data)
        else:
            print("I didn't find any tokens with that status.")
            print("\n")
    except Exception as e:
        print("Mongodb error: ", e)


leaderBoard = db["leader_board"]

def leaderBoardMongoBuild(all_rows):
    try:
        leaderBoard.insert_many(all_rows)
    except Exception as e:
        print("MongodDB error: ", e)

def leaderBoardMongoDestroy():
    try:
        leaderBoard.delete_many({})
    except Exception as e:
        print("MongodDB error: ", e)

def leaderBoardMongoReturn():
    cursor = leaderBoard.find({})
    result = list(cursor)
    return result

def leaderBoardMongoReturnSpecific(address):
    cursor = leaderBoard.find({"address":address})
    result = list(cursor)
    return result


    

    


