import pymongo
from rest_framework.exceptions import AuthenticationFailed
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ambluence_db"]
tokens = mydb['tokens']
agent_tokens = mydb['agent_tokens']
 

def token_required(func):
    def inner(request, *args, **kwargs):
      
        auth_header = request.headers.get('Authorization')
        a_token = auth_header.split()[1]
        details = tokens.find_one({"user_id":str(request.user._id),"access_token":a_token,"active":True})
        if details:
            return func(request, *args, **kwargs)
        else:
            raise AuthenticationFailed({'Message':'Token is blacklisted'})
         
    return inner


def agent_token_required(func):
    def inner(request, *args, **kwargs):
      
        auth_header = request.headers.get('Authorization')
        a_token = auth_header.split()[1]
        details = agent_tokens.find_one({"user_id":str(request.user._id),"access_token":a_token,"active":True})
        if details:
            return func(request, *args, **kwargs)
        else:
            raise AuthenticationFailed({'Message':'Token is blacklisted'})
         
    return inner


def agent_token_required(func):
    def inner(request, *args, **kwargs):
      
        auth_header = request.headers.get('Authorization')
        a_token = auth_header.split()[1]
        details = agent_tokens.find_one({"user_id":str(request.user._id),"access_token":a_token,"active":True})
        if details:
            return func(request, *args, **kwargs)
        else:
            raise AuthenticationFailed({'Message':'Token is blacklisted'})
         
    return inner