class ActivePool:
    def __init__(self):
    
        self.pool = {}

    def addToPool(self, user_obj):
        self.pool.update({user_obj.token_id: user_obj})
        return

    def removeFromPool(self, token_id):
        self.pool.pop(token_id)
        return

class UserObj:
    def __init__(self, token_id, handle):
        self.token_id = token_id
        self.handle = handle
        self.twitter_pfp_uri = ""
        self.state = 1
        self.status = False

    def Addpfp_uri(self, pfp_uri):
        self.twitter_pfp_uri = pfp_uri