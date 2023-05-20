import requests
from PIL import Image
import imagehash
from flask_restful import Resource
from flask import request
from . import database

import os
from dotenv import load_dotenv

load_dotenv()  

auth_token = os.environ.get("AUTH_TOKEN")  


def del_ext(directory, ext):

  for filename in os.listdir(directory):
    if filename.endswith(ext):
        os.remove(os.path.join(directory, filename))


def pfpCompare(token_id, twit_handle):

  url = f"https://api.twitter.com/2/users/by/username/{twit_handle}?user.fields=profile_image_url"
  
  headers = {
    "accept":
    "application/json",
    "Authorization":
    f"Bearer {auth_token}"
    }
  
  response = requests.get(url, headers=headers)
  
  pro_data = response.json()
  # print(pro_data)
  pro_pic = pro_data['data']['profile_image_url']
  
  pro_pic_edit = pro_pic.replace("_normal", "_400x400")
  
  # print(pro_pic_edit)
  
  import urllib.request
  urllib.request.urlretrieve(pro_pic_edit, "pfp.jpg")
  
  shq_token = f'https://s3.us-east-1.wasabisys.com/strangershq/shq_tkn/{token_id}.png'
  
  # print(shq_token)
  
  urllib.request.urlretrieve(shq_token, f'{token_id}.png')
  
  hash0 = imagehash.average_hash(Image.open(f'{token_id}.png'))
  hash1 = imagehash.average_hash(Image.open('pfp.jpg'))
  cutoff = 5
  # maximum bits that could be different between the hashes.

  #DELETE Media Files Downloaded

  directory = "/home/runner/strangers"  # Replace with the path to your directory

  # del_ext(directory, ".png")
  # del_ext(directory, ".jpg")


  #compare
  if hash0 - hash1 < cutoff:
    # print('images are similar')
    return [True, pro_pic_edit, shq_token]
  else:
    # print('images are not similar')
    return [False, pro_pic_edit, shq_token]
  

def twitterTracking(token_id, twit_handle):
   pfp_status = pfpCompare(token_id, twit_handle)
   if pfp_status[0] == True:
      database.dbUpdatePFP(token_id)
      return {"status":"Success", "pfp_status":True}
   else:
      database.dbUpdatePFPFalse(token_id)
      return {"status":"Success", "pfp_status":False}
    

class PFPTracking(Resource):

  def post(self):
    json_data = request.get_json(force=True)
    try:
        token_id = json_data['token_id']
        handle = json_data['handle']
        pfp_status = pfpCompare(token_id, handle)
        return {"pfp_status": pfp_status[0], "token_id": token_id, "twitter_id": handle,
                "twitter_url": pfp_status[1], "nft_url": pfp_status[2]}
    except:   
        result = {"status":"Failed", "errorMessage":"Incorrect Input"}
    return result, 201
  
class TwitterTracking(Resource):

  def post(self):
    json_data = request.get_json(force=True)
    try:
        token_id = json_data['token_id']
        handle = json_data['handle']
        result = twitterTracking(token_id, handle)
        return result
    except:   
        result = {"status":"Failed", "errorMessage":"Incorrect Input"}
    return result, 201  
