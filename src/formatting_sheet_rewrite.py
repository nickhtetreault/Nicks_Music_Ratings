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

def add_merge(range, merge_type, sheetId):
    convert_range = gspread.utils.a1_range_to_grid_range(range)
    return {
        "mergeCells": {
            "range": {
                "sheetId": sheetId,
                "startRowIndex": convert_range["startRowIndex"],
                "endRowIndex": convert_range["endRowIndex"],
                "startColumnIndex": convert_range["startColumnIndex"],
                "endColumnIndex": convert_range["endColumnIndex"]
            },
            "mergeType": merge_type
        }
    }

def add_format(range, bg, font_color, font_size, bold):
    return {
        "range": range,
        "format": {
            "backgroundColor": {
                "red": Colors[bg][0],
                "green": Colors[bg][1],
                "blue": Colors[bg][2]
            },
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE",
            "textFormat": {
                "foregroundColor": {
                    "red": Colors[font_color][0],
                    "green": Colors[font_color][1],
                    "blue": Colors[font_color][2]
                },
                "fontFamily": "Roboto Serif",
                "fontSize": font_size,
                "bold": bold
            }
        }
    }

# authorizing code to edit my spreadsheets with credentials (hidden)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("C:\\Users\\pickl\\OneDrive\\Desktop\\Nicks_music_ratings\\Credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# opening the spreadsheet
spreadsheet_id = "1Jc7roe2tmtVx-0hdn6DPI2zDh6NcPyWLBMVZN20a5WM"
sh = client.open_by_key(spreadsheet_id)

# Get artist data
token = get_token()
artist = Artist(token, "The Dillinger Escape Plan")
# create worksheet later once testing is done
worksheet = sh.worksheet(artist.artist_name)

sheetId = worksheet._properties['sheetId']

# worksheet.hide_gridlines()

# batch_update_album(worksheet, artist)


# Format requests for Artist name, album rankings, song rankings, comments
formats = []

# Formatting all cells (essentially background)
formats.append(add_format("A1:W500", "bg", "Black", 10, False))
# Artist name header
formats.append(add_format("B2:O4", "Gray_1", "Purple_1", 38, True))
# Album ratings header
formats.append(add_format("Q2:V4", "Gray_1", "Purple_1", 38, True))
# Album ratings data labels
formats.append(add_format("Q5:V5", "bg", "Purple_3", 10, True))
# Song ratings header
pos = 7 + len(artist.album_objects) # placing based on number of albums
formats.append(add_format(f"Q{pos}:V{pos + 2}", "Gray_1", "Purple_1", 38, True))
# Song ratings data labels
formats.append(add_format(f"Q{pos + 3}:V{pos + 3}", "bg", "Purple_3", 10, True))
# Comments header
formats.append(add_format(f"Q{pos + 15}:V{pos + 17}", "Gray_1", "Purple_1", 38, True))
# Comments text formatting
formats.append({
    "range": f"Q{pos + 18}:V{pos + 33}",
    "format": {
        "horizontalAlignment": "LEFT",
        "verticalAlignment" : "TOP",
        "wrapStrategy": "WRAP"
    }
})


# merges for everything idk lol
merges = []

# merging artist name header
merges.append(add_merge("B2:O4", "MERGE_ALL", sheetId))
# merging album rankings header
merges.append(add_merge("Q2:V4", "MERGE_ALL", sheetId))
# merging song rankings header
merges.append(add_merge(f"Q{pos}:V{pos + 2}", "MERGE_ALL", sheetId))
# merging comments header
merges.append(add_merge(f"Q{pos + 15}:V{pos + 17}", "MERGE_ALL", sheetId))
# merging comments text
merges.append(add_merge(f"Q{pos + 18}:V{pos + 33}", "MERGE_ALL", sheetId))

text = [ 
    {
        "range": "B2:O4",
        "values": [[artist.artist_name]]
    }
]

# Add album formatting and data to batch requests

worksheet.batch_format(formats)

body = {
    "requests": merges
}

# worksheet.batch_update(merges)

sh.batch_update(body)

worksheet.batch_update(text)