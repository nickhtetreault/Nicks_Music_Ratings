import os
import requests
from dotenv import load_dotenv
from filter_items import *

load_dotenv()
API_KEY = os.getenv("DISCOGS_KEY")
BASE_URL = 'https://api.discogs.com'

headers = {
    'Authorization': f'Discogs token={API_KEY}',
    'User-Agent': 'music_ratings'
}

def get_studio_albums(artist_name):
    response = requests.get(f"{BASE_URL}/database/search?type=master&&sort=year&artist={artist_name}&role=main&format=album", headers=headers)
    releases = response.json()
    count = 0
    albs = []
    for item in releases.get("results", []):
        formats = item.get("format", [])
        if "Compilation" not in formats and "Promo" not in formats and "Reissue" not in formats and "Unnofficial Release" not in formats and not check_bad(item.get("title", [])):
            title = item.get("title", []).split("-")[1].strip()
            albs.append(title)
            count += 1
    return albs
