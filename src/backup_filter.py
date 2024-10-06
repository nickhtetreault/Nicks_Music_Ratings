import google.generativeai as genai
from dotenv import load_dotenv
from artist_data import Artist
from artist_data import *
import os

   
def get_gemini_data(artist):
    load_dotenv()
    key = os.getenv("API_KEY")
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    album_titles = []
    for alb in artist.album_objects:
        album_titles.append(alb.album_title)
    print(album_titles)
    print("break\n\n\n\n")
    response = model.generate_content(f"Here is a list of albums released by {artist.artist_name}: {album_titles}. Return a list of the indices of albums in the provided list which are not studio albums (i.e. compilations, live releases, remixes, etc.). Do not add any albums that were not provided, and only respond with a list of indices which can be parsed in python.")
    print(response.text)
    data = response.text
    # cleaning response to be list of album titles
    indices = data[(data.find("[") + 1):data.find("]")].replace("\"", "").split(",")

    # removing whitespace
    for i in range(len(indices)):
        indices[i] = indices[i].lower().strip()

    return indices

token = get_token()
temp = Artist(token, "Dream Theater")
remove = get_gemini_data(temp)

# for num in remove:


# for alb in remove:
#     print(alb)