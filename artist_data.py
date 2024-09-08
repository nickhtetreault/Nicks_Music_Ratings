from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Getting access token for Spotify Web API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# object containing all data to be put into spreadsheet
class ArtistData:
    def __init__(self, token, artist_name):
        self.token = token
        self.artist_name = artist_name

        # finding artist_id
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        query = f"?q={artist_name}&type=artist&limit=1"
        query_url = url + query

        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]
        if len(json_result) == 0:
            print("No artist found with this name")
            return None
        else:
            self.artist_id = json_result[0]["id"]

class Album:
    def __init__(self, token, album_id):
        self.token = token
        self.album_id = album_id

    # def setAlbumData(self):




def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist found with this name")
        return None

    return json_result[0]

def get_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album&market=US&limit=50"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_songs(token, album_id):
    url = "https://api.spotify.com/v1/albums/2bVYeA0BEb0Rtj94ECaahK/tracks?market=US&limit=50&offset=0"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

token = get_token()

result = search_for_artist(token, "Opeth")

# print(result)

artist_id = result["id"]

albums = get_albums(token, artist_id)

# for i in range(len(albums["items"])):
    # print(albums["items"][i]["id"])
print(get_songs(token, albums["items"][15]["id"])["items"][0]["name"])

# print(len(albums["items"]))

# print(result["name"])
# print(artist_id)