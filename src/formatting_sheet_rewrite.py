import gspread
import time
import random
import requests
from gspread_formatting import *
from google.oauth2.service_account import Credentials
from artist_data import Artist, Album
from artist_data import *

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

# Exponential backoff retry function
def exponential_backoff(func, *args, max_retries=8, **kwargs):
    retries = 0
    while retries < max_retries:
        try:
            # Attempt the operation
            return func(*args, **kwargs)
        except (gspread.exceptions.APIError, requests.exceptions.RequestException) as e:
            # Log the error and handle the backoff
            # Calculate backoff time: base delay * (2^retries) + random jitter
            backoff_time = (2 ** retries) + random.uniform(0, 1)
            # print(f"Retrying in {backoff_time} seconds...")
            print(f"Request failed with {type(e).__name__}: {e}. Retrying in {backoff_time} seconds...")
            
            time.sleep(backoff_time)
            retries += 1
    
    # If max retries are exceeded, raise an exception
    raise Exception("Maximum retries exceeded")

def batch_update_album(worksheet, artist):
    batch_requests = []

    # Starting row for first album
    pos = 6

    for i in range(len(artist.album_objects) - 1, -1, -1):
        alb = artist.album_objects[i]
        alb_num = len(artist.album_objects) - i - 1
        
        # Prepare the batch request for album number, release date, title, etc.
        
        
        batch_requests.append({
            "range": f"C{pos}:C{pos + 1}",
            "values": [[alb_num + 1], [""]]
        })
        batch_requests.append({
            "range": f"D{pos}:D{pos + 1}",
            "values": [[alb.release_date], [""]]
        })
        batch_requests.append({
            "range": f"E{pos}:K{pos + 1}",
            "values": [[alb.album_title], [""]]
        })
        batch_requests.append({
            "range": f"M{pos}:N{pos + 1}",
            "values": [["Rating"], [""]]
        })
        # Track listing for the songs
        for j in range(len(alb.song_titles)):
            song_pos = pos + 3 + j

            batch_requests.append({
                "range": f"E{song_pos}",
                "values": [[j + 1]]
            })

            batch_requests.append({
                "range": f"F{song_pos}",
                "values": [[alb.song_titles[j]]]
            })

            batch_requests.append({
                "range": f"J{song_pos}",
                "values": [[alb.song_lens[j]]]
            })

        # Update row position for next album
        pos += 4 + len(alb.song_titles)

    # Execute the batch update with a single API call
    exponential_backoff(worksheet.batch_update, batch_requests)

# authorizing code to edit my spreadsheets with credentials (hidden)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("C:\\Users\\pickl\\OneDrive\\Desktop\\Nicks_music_ratings\\Credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# opening the spreadsheet
sheet_id = "1Jc7roe2tmtVx-0hdn6DPI2zDh6NcPyWLBMVZN20a5WM"
sh = client.open_by_key(sheet_id)


# Get artist data
token = get_token()
artist = Artist(token, "The Dillinger Escape Plan")
# create worksheet later once testing is done
worksheet = sh.worksheet(artist.artist_name)

worksheet.hide_gridlines()
# batch_update_album(worksheet, artist)


# Format requests for Artist name, album rankings, song rankings, comments
formats = [
    # Formatting all cells
    {
        "range": "A1:W500",
        "format": {
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
            },
        },
    },
    # Artist name header
    {
        "range": "B2:O4",
        "format": {
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
        }
    },
    # Album rankings header
    {
        "range": "Q2:V4",
        "format": {
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
        }
    },
    # Album rankings data labels
    {
        "range": "Q5:V5",
        "format": {
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE",
            "textFormat": {
            "foregroundColor": {
                "red": Colors["Purple_3"][0],
                "green": Colors["Purple_3"][1],
                "blue": Colors["Purple_3"][2]
            },
            "fontFamily" : "Roboto Serif",
            "fontSize": 10,
            "bold": True
            }
        }
    },
    {
        "range": f"Q{len(artist.album_objects) + 7}:V{len(artist.album_objects) + 9}",
        "format": {
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
        }
    },
    {
        "range": f"Q{len(artist.album_objects) + 10}:V{len(artist.album_objects) + 10}",
        "format": {
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE",
            "textFormat": {
            "foregroundColor": {
                "red": Colors["Purple_3"][0],
                "green": Colors["Purple_3"][1],
                "blue": Colors["Purple_3"][2]
            },
            "fontFamily" : "Roboto Serif",
            "fontSize": 10,
            "bold": True
            }
        }
    },
    {
        "range": f"Q{len(artist.album_objects) + 22}:V{len(artist.album_objects) + 24}",
        "format": {
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
        }
    }
]

# Apply the batch update to the sheet


worksheet.batch_format(formats)