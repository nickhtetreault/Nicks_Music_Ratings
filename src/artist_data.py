from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import re
import difflib
from filter_items import *
from discogs_filter import *

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

# computing similarity of names
def compute_similarity(input_name, found_name):
    diff = difflib.ndiff(input_name, found_name)
    diff_count = 0
    for line in diff:
        if line.startswith("-"):
            diff_count += 1
    return 1 - (diff_count / len(input_name))

# object containing all data to be put into spreadsheet
# also has variables that will be updated by input in spreadsheet (soon™)
class Artist:
    def __init__(self, artist_name):
        self.token = get_token()

        # structuring request & finding artist_id
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(self.token)
        query = f"?q={artist_name}&type=artist&limit=1"
        query_url = url + query
        result = get(query_url, headers=headers)
        # parsing json content to make data easier to accest
        json_result = json.loads(result.content)["artists"]["items"]
        similarity = compute_similarity(json_result[0]["name"], artist_name)

        # checking that artist with given name exists
        if len(json_result) == 0:
            raise Exception("No artist found with this name")
        
        # if (json_result[0]["name"].lower() != artist_name.lower()):
        #     name = json_result[0]["name"]
        #     raise Exception(f"Expected {artist_name} but found {name}")
        
        if (similarity < .75):
            name = json_result[0]["name"]
            raise Exception(f"Expected {artist_name} but found {name}")
        
        self.artist_name = json_result[0]["name"]
        self.artist_id = json_result[0]["id"]

        self.get_albums()
    
    def get_albums(self):
        # structuring request
        url = f"https://api.spotify.com/v1/artists/{self.artist_id}/albums?include_groups=album&market=US&limit=50"
        headers = get_auth_header(self.token)
        result = get(url, headers=headers)

        # parsing json content to make data easier to access
        album_data = json.loads(result.content)
        
        # creating Album objects with album id's
        num_albs = len(album_data["items"])

        album_titles = []
        for i in range(num_albs - 1, -1, -1):
            if album_titles:
                # checking if repeat of last album appended to list (imperfect)
                if album_titles[-1][0].lower() in album_data["items"][i]["name"].lower() or album_data["items"][i]["name"].lower() in album_titles[-1][0].lower():
                    # checking to see if title is shorter than previous title, meaning it's likely the original verison (the one I want)
                    if len(album_data["items"][i]["name"].lower()) < len(album_titles[-1][0].lower()):
                        album_titles[-1] = (album_data["items"][i]["name"], i)
                    else:
                        continue
                elif check_bad(album_data["items"][i]["name"]):
                    continue
                else:
                    album_titles.append((album_data["items"][i]["name"].strip(), i))
            else:
                album_titles.append((album_data["items"][i]["name"].strip(), i))
        
        studio_albs = get_studio_albums(self.artist_name)
   

        # I know this is like O(n^2) but the lists aren't gonna be that long and it seems overkill to implement
        # some algo to more efficiently search for similar strings in faster time
        # I would be inclined to try alb numer or release year but I'm worried about discrepencies between
        # Spoify API data and discogs data (more likely to break imo)
        album_objects = []
        for title, alb_num in album_titles:
            for studio_title in studio_albs:
                # removing punctuation, sometimes discrepency between spot & discogs (ex. Dream Theater)
                spot_title = re.sub(r'[^\w\s]', '', title.lower())
                discogs_title = re.sub(r'[^\w\s]', '', studio_title.lower())
                if spot_title in discogs_title or discogs_title in spot_title:
                    alb = Album(self.token, album_data, alb_num)
                    if (alb.album_len != "0:00"):
                        album_objects.append(alb)
                    studio_albs.remove(studio_title)

        self.album_objects = album_objects

# object containing all data from an album from spotify
# also has variables that will be updated by input in spreadsheet
class Album:
    def __init__(self, token, album_data, album_num):
        self.token = token
        self.album_data = album_data

        # deriving vars from album_data
        self.album_id = album_data["items"][album_num]["id"]
        self.release_date = album_data["items"][album_num]["release_date"][0:4] # getting year only
        self.album_title = clean_alb_title(album_data["items"][album_num]["name"], self.release_date)
        # self.album_title = real_title
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
            if not check_bad_song(s["name"]):
                song = clean_song_title(s["name"])
                song_titles.append(song)
                song_ids.append(s["id"])
                song_lens.append(self.millis_to_mins(s["duration_ms"]))
                # Keeping track of overall length of album to convert to hr:min:sec later
                album_len += s["duration_ms"]

        self.song_titles = song_titles
        self.song_ids = song_ids
        self.song_lens = song_lens
        self.album_len = self.millis_to_mins(album_len)

    # converting lengths of songs & albs to more readable hours:mins:seconds (ex. 1:04:23, 2:06, 10:04, etc.)
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
            return f"{hours}:{minutes}:{seconds}"


# \/\/\/ TEST CODE \/\/\/

# try: 
#     artist = Artist("Opeth")
# except Exception as e:
#     print(f"Error: {str(e)}")

# num_albs = len(artist.album_objects)

# artist = Artist("Haken")

# for i, alb in enumerate(artist.album_objects):
#     print(f"{i + 1} {alb.album_title} {alb.release_date} {alb.album_len}")
#     for i in range(len(alb.song_titles)):
#         print(alb.song_titles[i] + " " + alb.song_lens[i])
#     print("\n")

# print(num_albs)