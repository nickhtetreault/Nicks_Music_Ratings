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
class Artist:
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
        headers = get_auth_header(self.token)
        result = get(url, headers=headers)

        # parsing json content to make data easier to access
        album_data = json.loads(result.content)

        album_objects = []
        
        # creating Album objects with album id's
        for i in range(len(album_data["items"])):
            album = Album(self.token, album_data, i)
            album_objects.append(album)

        # self.album_titles = album_titles
        self.album_objects = album_objects


# object containing all data from an album from spotify
# also has variables that will be updated by input in spreadsheet
class Album:
    def __init__(self, token, album_data, album_num):
        self.token = token
        self.album_data = album_data

        # deriving vars from album_data
        self.album_id = album_data["items"][album_num]["id"]
        self.album_title = album_data["items"][album_num]["name"]
        self.release_date = album_data["items"][album_num]["release_date"][0:4]
        self.cover = album_data["items"][album_num]["images"][0]["url"]
        self.get_song_data()

    def get_song_data(self):
        # structuring request
        url = f"https://api.spotify.com/v1/albums/{self.album_id}/tracks?market=US&limit=50&offset=0"
        headers = get_auth_header(self.token)
        result = get(url, headers=headers)

        # parsing json content again
        song_data = json.loads(result.content)
        self.song_data = song_data

        # adding song titles to song list
        song_titles = []
        # probably won't need ids for now
        # might be useful for later implementations
        # might convert to a map later (song_title -> song_rating)
        song_ids = []
        song_lens = []
        album_len = 0
        # Assigning data for each song on the album
        for s in song_data["items"]:
            song_titles.append(s["name"])
            song_ids.append(s["id"])
            song_lens.append(self.millis_to_mins(s["duration_ms"]))
            # Keeping track of overall length of album to convert to hr:min:sec later
            album_len += s["duration_ms"]

        self.song_titles = song_titles
        self.song_ids = song_ids
        self.song_lens = song_lens
        self.album_len = self.millis_to_mins(album_len)

    # converting song lengths to more readable mins:seconds (ex. 4:23, 2:06, 10:04, etc.)
    def millis_to_mins(self, millis):
        # if song is shorter than one hour (99.999999% of cases)
        if (millis < 3600000):
            seconds = int(millis/1000)%60
            minutes = int(millis/(1000*60))%60
            if (seconds < 10):
                seconds = "0" + str(seconds)
            return f"{minutes}:{seconds}"
        else:
            seconds = int(millis/1000)%60
            minutes = int(millis/(1000*60))%60
            hours = int(millis/(1000*60*60))%24
            if (seconds < 10):
                seconds = "0" + str(seconds)
            if (minutes < 10):
                minutes = "0" + str(minutes)
            return f"{minutes}:{seconds}:{hours}"
