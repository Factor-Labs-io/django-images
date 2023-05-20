import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  

url = os.environ.get("DATABASE_URL")  
connection = psycopg2.connect(url)


########### Table: Wallet Information  ########### 
QUERY_ALL = "select * from wallet_information;"
QUERY_LEADER_BOARD = "select * from wallet_information order by points desc;"
QUERY_ROW =   "select * from wallet_information where address = (%s);"
QUERY_TOKEN = "select token_id from wallet_information where address = (%s);"
QUERY_POINTS = "select points from wallet_information where address = (%s);"
QUERY_HANDLE = "select twitter_id from wallet_information where address = (%s);"
QUERY_BY_HANDLE = "select * from wallet_information where twitter_id = (%s);"
QUERY_PFP = "select pfp_status from wallet_information where address = (%s);"
INSERT_USER  = "insert into wallet_information(address, twitter_id, token_id, twitter_pfp_url, hometown, discord_handle, interests)\
                values ((%s), (%s), (%s),(%s), (%s), (%s), (%s));"
UPDATE_HANDLE = "update wallet_information set twitter_id = (%s) where address = (%s);"
UPDATE_TOKEN = "update wallet_information set token_id = (%s) where address = (%s);"
UPDATE_PFPSTATUS = "update wallet_information set pfp_status = true where token_id = (%s);"
UPDATE_PFPSTATUS_FALSE = "update wallet_information set pfp_status = false where token_id = (%s);"
UPDATE_PFPSTATUS_ADDRESS = "update wallet_information set pfp_status = (%s) where address = (%s);"
UPDATE_POINTS = "update wallet_information set points = (%s) where address = (%s);"
POINTS_AGG = "select points from aggregate_points_score limit 1;"
POINTS_MULTIPLIER = "update aggregate_points_score set points = (%s);"
UPDATE_POINTS_AGG = "update wallet_information set points = points+(%s) where token_id = (%s);"
UPDATE_URL = "update wallet_information set twitter_pfp_url = (%s) where address = (%s);"
UPDATE_HOMETOWN = "update wallet_information set hometown = (%s) where address = (%s);"
UPDATE_DISCORD = "update wallet_information set discord_handle = (%s) where address = (%s);"
UPDATE_INTERESTS= "update wallet_information set interests = (%s) where address = (%s);"
DELETE_ROW =   "delete from wallet_information where address = (%s);"
########### Table: Point Transaction History  ###########



def dbQueryAll():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_ALL)
            rows = cursor.fetchall()
            mydict = {}
            for i, row in enumerate(rows):
                key = f"Row {i}" 
                value = {"address": row[0], "twitter_id": row[1], "token_id": row[2], "pfp_status": row[3], "points": row[4],
                         "twitter_pfp_url":row[5],"hometown":row[6],"discord_handle":row[7],"interests":row[8]}
                mydict[key] = value        
    return mydict 

def dbQueryLeaderBoard():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_LEADER_BOARD)
            rows = cursor.fetchall()
            mylist = []
            for i, row in enumerate(rows):
                value = {"_id": 0,"address": row[0], "twitter_id": row[1], "token_id": row[2], "pfp_status": row[3], "points": row[4],
                         "twitter_pfp_url":row[5],"hometown":row[6],"discord_handle":row[7],"interests":row[8]}
                mylist.append(value)        
    return mylist 

def dbQueryRow(address):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_ROW, (address,))
            row = cursor.fetchone()
            if row is not None:
                address = row[0]
                handle = row[1]
                token = row[2]
                pfp_status = row[3]
                points = row[4]
                twitter_url = row[5]
                hometown = row[6]
                discord_handle = row[7]
                interests = row[8]
                result =  {
                    "address": address,
                    "twitter_id": handle,
                    "token_id": token,
                    "pfp_status": pfp_status,
                    "points": points,
                    "twitter_pfp_url": twitter_url,
                    "hometown": hometown,
                    "discord_handle": discord_handle,
                    "interests": interests
                }
                return {"status": "Success", "data": result}
            else:
                return {"status": "Error", "message": "No row found for the given address"}
# def dbQueryRow(address):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(QUERY_ROW, (address,))
#             row = cursor.fetchone()
#             print(row)
#             address = row[0]
#             handle = row[1]
#             token = row[2]
#             pfp_status = row[3]
#             points = row[4]
#             twitter_url = row[5]
#             hometown = row[6]
#             discord_handle = row[7]
#             interests = row[8]
#             result =  {"address": address, "twitter_id": handle, "token_id":token, "pfp_status":pfp_status, 
#                        "points":points, "twitter_pfp_url": twitter_url,
#                        "hometown":hometown,"discord_handle":discord_handle,"interests":interests}
#     return {"status": "Success", "data": result }

def dbQueryByHandle(handle):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_BY_HANDLE, (handle,))
            row = cursor.fetchone()
            address = row[0]
            handle = row[1]
            token = row[2]
            pfp_status = row[3]
            points = row[4]
            twitter_url = row[5]
            hometown = row[6]
            discord_handle = row[7]
            interests = row[8]
            result =  {"address": address, "twitter_id": handle, "token_id":token, "pfp_status":pfp_status, 
                       "points":points, "twitter_pfp_url": twitter_url,
                       "hometown":hometown,"discord_handle":discord_handle,"interests":interests}
    return {"status": "Success", "data": result }

def dbQueryToken(address):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_TOKEN, (address,))
            token_id = cursor.fetchone()[0]
            result =  {"token_id": token_id}
    return {"status": "Success", "data": result }

def dbAddUser(address, handle, token, twitter_url, hometown, disc_handle, interests):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (address, handle, token, twitter_url, hometown, disc_handle, interests,))
    return {"status": "Success"}

def dbUpdateUser(address, handle, token):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_ROW, (address,))
            if cursor.fetchone() == None:
                cursor.execute(INSERT_USER, (address, handle, token,))
                return {"status": "Success"}
            else:
                cursor.execute(UPDATE_HANDLE, (handle, address,))
                cursor.execute(UPDATE_TOKEN, (token, address,))
                return {"status": "Success"}    

def dbUpdatePostgre(address, handle, token, pfp_status, points):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_ROW, (address,))
            if cursor.fetchone() == None:
                cursor.execute(INSERT_USER, (address, handle, token,))
                return {"status": "Success"}
            else:
                cursor.execute(UPDATE_HANDLE, (handle, address,))
                cursor.execute(UPDATE_TOKEN, (token, address,))
                cursor.execute(UPDATE_PFPSTATUS_ADDRESS, (pfp_status, address,))
                cursor.execute(UPDATE_POINTS, (points, address,))
                return {"status": "Success"}  

def dbQueryPoints(address):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_POINTS, (address,))
            points = cursor.fetchone()[0]
            result =  {"points": points}
    return {"status": "Success", "data": result }   

def dbQueryHandle(address):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_HANDLE, (address,))
            handle = cursor.fetchone()[0]
            result =  {"twitter_id": handle}
    return {"status": "Success", "data": result }      

def dbQueryPFP(address):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_PFP, (address,))
            pfp_status = cursor.fetchone()[0]
            result =  {"pfp_status": pfp_status}
    return {"status": "Success", "data": result }

def dbUpdatePFP(token):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_PFPSTATUS, (token,))
    return {"status": "Success"}

def dbUpdatePFPFalse(token):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_PFPSTATUS_FALSE, (token,))
    return {"status": "Success"}

def dbUpdatePoints(token):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(POINTS_AGG)
            pfp_agg = cursor.fetchone()[0]
            cursor.execute(UPDATE_POINTS_AGG, (pfp_agg, token,))
    return {"status": "Success"}

def dbUpdateTokenID(address, token):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_TOKEN, (token, address,))
    return {"status": "Success"}

def dbUpdateURL(address, twitter_pfp_url):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_URL, (twitter_pfp_url, address,))
    return {"status": "Success"}   

def dbUpdateHometown(address, hometown):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_HOMETOWN, (hometown, address,))
    return {"status": "Success"}   

def dbUpdateDiscord(address, disc_handle):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_DISCORD, (disc_handle, address,))
    return {"status": "Success"}   

def dbUpdateInterests(address, interests):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_INTERESTS, (interests, address,))
    return {"status": "Success"}  

def dbPointsMultiplier(points):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(POINTS_MULTIPLIER, (points,))
    return {"status": "Success"} 

def dbDeleteRow(address):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ROW, (address,))
    return {"status": "Success"}   

