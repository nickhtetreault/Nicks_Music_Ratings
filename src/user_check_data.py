import gspread
from gspread_formatting import *
from google.oauth2.service_account import Credentials
# from artist_data import Artist
from artist_data import *
from batch_formatting_sheet import add_format, add_merge, add_text

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("C:\\Users\\pickl\\OneDrive\\Desktop\\Nicks_music_ratings\\Credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# opening the spreadsheet
spreadsheet_id = "1Jc7roe2tmtVx-0hdn6DPI2zDh6NcPyWLBMVZN20a5WM"
sh = client.open_by_key(spreadsheet_id)

# setting up sheet to have user confirm cleaned catalogue data
def confirm_data(artist_name):
    try: 
        artist = Artist(artist_name)
    except Exception as e:
        raise Exception(e)
    
    worksheet = sh.add_worksheet(title=artist_name, rows=1000, cols=23)
    sheetId = worksheet._properties['sheetId']

    data = []
    merges = []
    formats = []

    formats.append(add_format("A1:J90", "White", "Black", 10, False))

    merges.append(add_merge(f"C2:F{len(artist.album_objects) + 2}", "MERGE_ROWS", sheetId))
    merges.append(add_merge(f"H3:I3", "MERGE_ALL", sheetId))
    
    data.append(add_text("B2:B2", "Year"))
    data.append(add_text("C2:F2", "Album Title"))
    data.append(add_text("H3:I3", "Confirm? (Y/N)"))
    data.append(add_text("J2:J2", "↓ Here ↓"))

    for i, alb in enumerate(artist.album_objects):
        data.append(add_text(f"B{3 + i}:B{3 + i}", alb.release_date))
        data.append(add_text(f"C{3 + i}:F{3 + i}", alb.album_title))

    worksheet.batch_format(formats)
    merge = {
        "requests": merges
    }
    sh.batch_update(merge)
    worksheet.batch_update(data)