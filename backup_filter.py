import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("API_KEY")

genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Get the titles of every core studio albums by artist The Mars Volta. Return this in the form of a list of strings to be parsed in python.")
print(response.text)