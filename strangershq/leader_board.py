from . import database, mongo_interact, infura
from flask_restful import Resource
from flask import request   

def leaderBoardBuild():
    all_rows = leaderBoardFinalTally()
    mongo_interact.leaderBoardMongoBuild(all_rows)

def leaderBoardDestory():
    mongo_interact.leaderBoardMongoDestroy()

def leaderBoardReturn():
    result = mongo_interact.leaderBoardMongoReturn()
    return result

def leaderBoardReturnSpecific(json_data):
    address = json_data['address']
    result = mongo_interact.leaderBoardMongoReturnSpecific(address)
    return result

def leaderBoardSorting(all_rows):
    sortedPoints = sorted(all_rows, key=lambda d: d['points'], reverse=True)
    return sortedPoints 

def leaderBoardRanking(all_rows):
    for i, dict in enumerate(all_rows):
        dict["_id"] = i+1
    return all_rows

def leaderBoardCombinePoints():
    all_rows = database.dbQueryLeaderBoard()
    for dict in all_rows:
        onChainPoints = infura.getOnChainPoints(dict["address"])
        dict["points"] += onChainPoints
    return all_rows

def leaderBoardFinalTally():
    points = leaderBoardCombinePoints()
    sortedPoints = leaderBoardSorting(points)
    result = leaderBoardRanking(sortedPoints)
    return result


class LeaderBoardBuild(Resource):

    def get(self):
        try:
            leaderBoardBuild()
            result = {"status":"Success"}
        except:   
            result = {"status":"Failed"}
        return result, 201
    
class LeaderBoardDestory(Resource):

    def get(self):
        try:
            leaderBoardDestory()
            result = {"status":"Success"}
        except:   
            result = {"status":"Failed"}
        return result, 201    

class LeaderBoardReturn(Resource):

    def get(self):
        try:
            results = leaderBoardReturn()
            result = {"status":"Success", "data": results}
        except:   
            result = {"status":"Failed"}
        return result, 201


class LeaderBoardFetch(Resource):

    def get(self):
        try:
            results = leaderBoardReturn()
            result = {"status":"Success", "data": results}
        except:   
            result = {"status":"Failed"}
        return result, 201
    
class LeaderBoardFetchSpecific(Resource):

    def post(self):
        try:
            json_data = request.get_json(force=True)
            results = leaderBoardReturnSpecific(json_data)
            result = {"status":"Success", "data": results}
        except:   
            result = {"status":"Failed"}
        return result, 201
