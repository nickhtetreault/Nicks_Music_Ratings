import google.generativeai as genai
from dotenv import load_dotenv
import os

   
def get_gemini_data(artist_name):
    load_dotenv()
    key = os.getenv("API_KEY")
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Get the titles of every core studio albums by artist {artist_name}. Return this in the form of a list of strings to be parsed in python.")
    print(response.text)
    data = response.text
    # cleaning respons to be list of album titles
    albs = data[(data.find("[") + 1):data.find("]")].replace("\"", "").split(",")

    # removing whitespace
    for i in range(len(albs)):
        albs[i] = albs[i].strip()

    return albs

albs = get_gemini_data("Vacations")

for alb in albs:
    print(alb)