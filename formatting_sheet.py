import gspread
import time
import random
from gspread_formatting import *
from google.oauth2.service_account import Credentials
from artist_data import Artist, Album
from artist_data import *

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
        except gspread.exceptions.APIError as e:
            # Calculate backoff time: base delay * (2^retries) + random jitter
            backoff_time = (2 ** retries) + random.uniform(0, 1)
            print(f"Request failed with error: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            retries += 1
    
    raise Exception("Maximum retries exceeded")

def format_album(worksheet, alb, pos, i):
    # Album number
    exponential_backoff(worksheet.format, f"C{pos}:C{pos + 1}", {
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
        "fontSize": 25,
        "bold": True
        }    
    })
    exponential_backoff(worksheet.merge_cells, f"C{pos}:C{pos + 1}")
    exponential_backoff(worksheet.update_acell, f"C{pos}", i + 1)
    
    # Album release year
    exponential_backoff(worksheet.format, f"D{pos}:D{pos + 1}", {
    "backgroundColor": {
        "red": Colors["Gray_2"][0],
        "green": Colors["Gray_2"][1],
        "blue": Colors["Gray_2"][2]
    },
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "foregroundColor": {
            "red": Colors["Blue"][0],
            "green": Colors["Blue"][1],
            "blue": Colors["Blue"][2]
        },
        "fontFamily": "Roboto Serif",
        "fontSize": 25,
        "bold": True
        }    
    })
    exponential_backoff(worksheet.merge_cells, f"D{pos}:D{pos + 1}")
    exponential_backoff(worksheet.update_acell, f"D{pos}", alb.release_date)

    # Album title
    exponential_backoff(worksheet.format, f"E{pos}:K{pos + 1}", {
    "backgroundColor": {
        "red": Colors["Gray_3"][0],
        "green": Colors["Gray_3"][1],
        "blue": Colors["Gray_3"][2]
    },
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "foregroundColor": {
            "red": Colors["Purple_2"][0],
            "green": Colors["Purple_2"][1],
            "blue": Colors["Purple_2"][2]
        },
        "fontFamily": "Roboto Serif",
        "fontSize": 25,
        "bold": True
        }    
    })
    exponential_backoff(worksheet.merge_cells, f"E{pos}:K{pos + 1}")
    exponential_backoff(worksheet.update_acell, f"E{pos}", alb.album_title)

    # Album rating

    exponential_backoff(worksheet.format, f"M{pos}:N{pos + 1}", {
    "backgroundColor": {
        "red": Colors["Gray_3"][0],
        "green": Colors["Gray_3"][1],
        "blue": Colors["Gray_3"][2]
    },
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "foregroundColor": {
            "red": Colors["Purple_2"][0],
            "green": Colors["Purple_2"][1],
            "blue": Colors["Purple_2"][2]
        },
        "fontFamily": "Roboto Serif",
        "fontSize": 25,
        "bold": True
        }    
    })
    exponential_backoff(worksheet.merge_cells, f"M{pos}:N{pos + 1}")
    exponential_backoff(worksheet.update_acell, f"M{pos}", "Rating")

    # Rating input
    exponential_backoff(worksheet.format, f"M{pos + 2}:N{pos + 3}", {
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "fontFamily": "Roboto Serif",
        "fontSize": 20,
        "bold": True
        }    
    })
    exponential_backoff(worksheet.merge_cells, f"M{pos + 2}:N{pos + 3}")

    # Labels (song number, track title, length, rating)
    exponential_backoff(worksheet.format, f"E{pos + 2}:K{pos + 2}", {
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
        "foregroundColor": {
            "red": Colors["Purple_3"][0],
            "green": Colors["Purple_3"][1],
            "blue": Colors["Purple_3"][2]
        },
        "fontFamily": "Roboto Serif",
        "fontSize": 10,
        "bold": True
        }    
    })
    exponential_backoff(worksheet.merge_cells, f"F{pos + 2}:I{pos + 2}")
    exponential_backoff(worksheet.update_acell, f"E{pos + 2}", "#")   
    exponential_backoff(worksheet.update_acell, f"F{pos + 2}", "Song")
    exponential_backoff(worksheet.update_acell, f"J{pos + 2}", "Length")
    exponential_backoff(worksheet.update_acell, f"K{pos + 2}", "Rating")

    # Formatting songs
    for i in range(len(alb.song_titles)):
        exponential_backoff(worksheet.merge_cells, f"F{pos + 3 + i}:I{pos + 3 + i}")
        exponential_backoff(worksheet.update_acell, f"E{pos + 3 + i}", i + 1)   
        exponential_backoff(worksheet.update_acell, f"F{pos + 3 + i}", alb.song_titles[i])
        exponential_backoff(worksheet.update_acell, f"J{pos + 3 + i}", alb.song_lens[i])

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

# Get artist data
token = get_token()
artist = Artist(token, "Opeth")
worksheet = sh.worksheet(artist.artist_name)

worksheet.hide_gridlines()

# Setting background color & font for all cells
exponential_backoff(worksheet.format, "A1:W500", {
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
exponential_backoff(worksheet.format, "Q2:V4", {
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

# Merge album ranking cells and update
exponential_backoff(worksheet.merge_cells, "Q2:V4")
exponential_backoff(worksheet.update_acell, "Q2", "Album Rankings")

exponential_backoff(worksheet.format, "Q5:V5", {
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
})

exponential_backoff(worksheet.merge_cells, "R5:U5")

exponential_backoff(worksheet.update_acell, "Q5", "#")
exponential_backoff(worksheet.update_acell, "R5", "Title")
exponential_backoff(worksheet.update_acell, "V5", "Rating")

# Adding album numbers and merging cells
for i in range(len(artist.album_objects)):
    exponential_backoff(worksheet.update_acell, f"Q{6 + i}", i + 1)
    exponential_backoff(worksheet.merge_cells, f"R{6 + i}:U{6 + i}")

# Formatting song rankings
pos = 7 + len(artist.album_objects)

exponential_backoff(worksheet.format, f"Q{pos}:V{pos + 2}", {
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

# Merge song ranking header cells
exponential_backoff(worksheet.merge_cells, f"Q{pos}:V{pos + 2}")
exponential_backoff(worksheet.update_acell, f"Q{pos}", "Top 10 Songs")

exponential_backoff(worksheet.format, f"Q{pos + 3}:V{pos + 3}", {
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
})

# Add song ranking headers
exponential_backoff(worksheet.merge_cells, f"R{pos + 3}:U{pos + 3}")
exponential_backoff(worksheet.update_acell, f"Q{pos + 3}", "#")
exponential_backoff(worksheet.update_acell, f"R{pos + 3}", "Title")
exponential_backoff(worksheet.update_acell, f"V{pos + 3}", "Rating")

# Add song rankings
for i in range(10):
    exponential_backoff(worksheet.update_acell, f"Q{pos + 4 + i}", i + 1)
    exponential_backoff(worksheet.merge_cells, f"R{pos + 4 + i}:U{pos + 4 + i}")

# Add Comments
exponential_backoff(worksheet.format, f"Q{pos + 15}:V{pos + 17}", {
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

exponential_backoff(worksheet.merge_cells, f"Q{pos + 15}:V{pos + 17}")
exponential_backoff(worksheet.update_acell, f"Q{pos + 15}", "Comments")

exponential_backoff(worksheet.merge_cells, f"Q{pos + 18}:V{pos + 33}")
exponential_backoff(worksheet.format, f"Q{pos + 18}", {
    "horizontalAlignment": "LEFT",
    "verticalAlignment" : "TOP",
    "wrapStrategy": "WRAP"
})

# Starting row for first album, same for every spreadsheet
pos = 6

# Formatting every album, iterating thru album_objects backwards so
#   albums are displayed in chronological order
for i in range(len(artist.album_objects) - 1, -1, -1):
    alb_num = len(artist.album_objects) - i - 1
    format_album(worksheet, artist.album_objects[i], pos, alb_num)
    pos += 4 + len(artist.album_objects[i].song_titles)