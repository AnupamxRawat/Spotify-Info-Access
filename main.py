from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json

load_dotenv() #automatically load environment files. the .env file should be in same directory as main file
 
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")



def get_token():
    auth_string=client_id+":"+client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes),"utf-8")

    url="Https://accounts.spotify.com/api/token"
    headers={
        "Authorization":"Basic "+ auth_base64,
        "Content-type":"application/x-www-form-urlencoded"
    }

    data= {"grant_type":"client_credentials"}
    result=post(url,headers=headers,data=data)
    json_result=json.loads(result.content)
    token=json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization":"Bearer "+token}

def search_for_artist(token,artist_name):
    url="Https://api.spotify.com/v1/search"
    headers=get_auth_header(token)
    query=f"?q={artist_name}&type=artist&limit=1"
    query_url=url + query
    result=get(query_url,headers=headers)
    json_result=json.loads(result.content)["artists"]["items"]
    if(len(json_result)==0):
        print("No artist with this name exist!!")
        return None
    return json_result[0]
            
def get_songs_by_arist(token,artist_id):
    url=f"Https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers=get_auth_header(token)
    result=get(url,headers=headers)
    json_result=json.loads(result.content)["tracks"]
    songs= json_result
    print("Popular Songs of the Artists: ")
    for idx,song in enumerate(songs):
     print(f"{idx+1}.{song['name']}")

token=get_token()
result=search_for_artist(token,"Travis")
artist_id=result["id"]
get_songs_by_arist(token,artist_id)
