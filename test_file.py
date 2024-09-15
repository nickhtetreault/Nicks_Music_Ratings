import gspread
import time
import random
from gspread_formatting import *
from google.oauth2.service_account import Credentials
from artist_data import Artist, Album
from artist_data import *

# Exponential backoff retry function
def exponential_backoff(func, *args, max_retries=5, **kwargs):
    retries = 0
    while retries < max_retries:
        try:
            # Attempt the operation
            return func(*args, **kwargs)
        except gspread.exceptions.APIError as e:
            # Calculate backoff time: base delay * (2^retries) + random jitter
            backoff_time = (2 ** retries) + random.uniform(0, 1)
            print(f"Request failed with error: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            retries += 1
    
    raise Exception("Maximum retries exceeded")

# For my own reference lol \/\/\/
# command for running venv: .\venv\Scripts\activate.ps1

# authorizing code to edit my spreadsheets with credentials (hidden)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# opening the spreadsheet
sheet_id = "1Jc7roe2tmtVx-0hdn6DPI2zDh6NcPyWLBMVZN20a5WM"
sh = client.open_by_key(sheet_id)

# defining color hex codes for formatting
Colors = {
    "bg": [207 / 255.0, 226 / 255.0, 243 / 255.0],
    "Gray_1": [183 / 255.0, 183 / 255.0, 183 / 255.0],
    "Gray_2": [204 / 255.0, 204 / 255.0, 204 / 255.0],
    "Gray_3": [217 / 255.0, 217 / 255.0, 217 / 255.0],
    "Purple_1": [103 / 255.0, 78 / 255.0, 167 / 255.0],
    "Purple_2": [142 / 255.0, 124 / 255.0, 195 / 255.0],
    "Purple_3": [180 / 255.0, 167 / 255.0, 214 / 255.0],
    "Blue": [61 / 255.0, 133 / 255.0, 198 / 255.0],
    "Black": [0, 0, 0]
}

# Get artist data
token = get_token()
artist = Artist(token, "Opeth")
worksheet = sh.worksheet(artist.artist_name)

# Setting background color & font for all cells
exponential_backoff(worksheet.format, "A1:V500", {
    "backgroundColor": {
        "red": Colors["bg"][0],
        "green": Colors["bg"][1],
        "blue": Colors["bg"][2]
    },
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "fontFamily": "Roboto Serif",
        "fontSize": 10
    }
})

# Formatting header
exponential_backoff(worksheet.format, "B2:O4", {
    "backgroundColor": {
        "red": Colors["Gray_1"][0],
        "green": Colors["Gray_1"][1],
        "blue": Colors["Gray_1"][2]
    },
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "foregroundColor": {
            "red": Colors["Purple_1"][0],
            "green": Colors["Purple_1"][1],
            "blue": Colors["Purple_1"][2]
        },
        "fontFamily": "Roboto Serif",
        "fontSize": 38,
        "bold": True
    }
})

# Merge header cells and update artist name
exponential_backoff(worksheet.merge_cells, "B2:O4")
exponential_backoff(worksheet.update_acell, "B2", artist.artist_name)

# Formatting album rankings
exponential_backoff(worksheet.format, "Q2:U4", {
    "backgroundColor": {
        "red": Colors["Gray_1"][0],
        "green": Colors["Gray_1"][1],
        "blue": Colors["Gray_1"][2]
    },
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "foregroundColor": {
            "red": Colors["Purple_1"][0],
            "green": Colors["Purple_1"][1],
            "blue": Colors["Purple_1"][2]
        },
        "fontFamily": "Roboto Serif",
        "fontSize": 32,
        "bold": True
    }
})

# Merge album ranking cells and update
exponential_backoff(worksheet.merge_cells, "Q2:U4")
exponential_backoff(worksheet.update_acell, "Q2", "Album Rankings")

# Adding album numbers and merging cells
for i in range(len(artist.album_objects)):
    exponential_backoff(worksheet.update_acell, f"Q{6 + i}", i + 1)
    exponential_backoff(worksheet.merge_cells, f"R{6 + i}:T{6 + i}")

# Formatting song rankings
pos = 7 + len(artist.album_objects)

exponential_backoff(worksheet.format, f"Q{pos}:U{pos + 2}", {
    "backgroundColor": {
        "red": Colors["Gray_1"][0],
        "green": Colors["Gray_1"][1],
        "blue": Colors["Gray_1"][2]
    },
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "foregroundColor": {
            "red": Colors["Purple_1"][0],
            "green": Colors["Purple_1"][1],
            "blue": Colors["Purple_1"][2]
        },
        "fontFamily": "Roboto Serif",
        "fontSize": 32,
        "bold": True
    }
})

# Merge song ranking header cells
exponential_backoff(worksheet.merge_cells, f"Q{pos}:U{pos + 2}")
exponential_backoff(worksheet.update_acell, f"Q{pos}", "Top 10 Songs")

# Add song ranking headers
exponential_backoff(worksheet.merge_cells, f"R{pos + 3}:T{pos + 3}")
exponential_backoff(worksheet.update_acell, f"Q{pos + 3}", "#")
exponential_backoff(worksheet.update_acell, f"R{pos + 3}", "Title")
exponential_backoff(worksheet.update_acell, f"U{pos + 3}", "Rating")

# Add song rankings
for i in range(10):
    exponential_backoff(worksheet.update_acell, f"Q{pos + 4 + i}", i + 1)
    exponential_backoff(worksheet.merge_cells, f"R{pos + 4 + i}:T{pos + 4 + i}")

print("Worksheet formatting and data update completed successfully!")