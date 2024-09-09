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
# also has variables that will be updated by input in spreadsheet
class ArtistData:
    def __init__(self, token, artist_name):
        self.token = token
        self.artist_name = artist_name

        # structuring request & finding artist_id
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        query = f"?q={artist_name}&type=artist&limit=1"
        query_url = url + query
        result = get(query_url, headers=headers)
        # parsing json content to make data easier to accest
        json_result = json.loads(result.content)["artists"]["items"]

        # checking that artist with given name exists
        if len(json_result) == 0:
            print("No artist found with this name")
            return None
        self.artist_id = json_result[0]["id"]

        # calling get_albums, breaking up the functions so I don't have to put everything in init
        self.get_albums()
    
    def get_albums(self):
        # structuring request
        url = f"https://api.spotify.com/v1/artists/{self.artist_id}/albums?include_groups=album&market=US&limit=50"
        headers = get_auth_header(token)
        result = get(url, headers=headers)

        # parsing json content to make data easier to access
        album_data = json.loads(result.content)

        # might get rid of album titles later (redundant with Album objects)
        album_titles = []
        album_objects = []

        # \/\/\/ test variable \/\/\/
        # album_ids = []
        
        # creating Album objects with album id's
        for a in album_data["items"]:
            # album_ids.append(a["id"])
            album_titles.append(a["name"])
            album = Album(token, a["id"], album_data)
            album_objects.append(album)
        self.album_titles = album_titles
        self.album_objects = album_objects

        # test var
        # self.album_ids = album_ids

# object containing all data from an album from spotify
# also has variables that will be updated by input in spreadsheet
class Album:
    def __init__(self, token, album_id, album_data):
        self.token = token
        self.album_id = album_id
        self.album_data = album_data

        # calling get_songs() to break up the class
        self.get_song_data()

    def get_song_data(self):
        # structuring request
        url = f"https://api.spotify.com/v1/albums/{self.album_id}/tracks?market=US&limit=50&offset=0"
        headers = get_auth_header(token)
        result = get(url, headers=headers)

        # parsing json content again
        song_data = json.loads(result.content)
        self.song_data = song_data

        # adding song titles to song list
        song_titles = []
        # print(song_data)
        for s in song_data["items"]:
            song_titles.append(s["name"])
        self.song_titles = song_titles


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

opeth = ArtistData(token, "Opeth")

# print(opeth.album_ids)
# for id in opeth.album_ids:
#     print(id)

for s in opeth.album_objects[13].song_titles:
    print(s)

# print(opeth.album_objects[13].song_data)