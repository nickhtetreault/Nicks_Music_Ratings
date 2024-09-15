import gspread
import time
from gspread_formatting import *
from google.oauth2.service_account import Credentials
from artist_data import Artist, Album
from artist_data import *

# For my own reference lol \/\/\/
# command for running venv: .\venv\Scripts\activate.ps1

# authorizing code to edit my spreadsheets with credentials (hidden)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes = scopes)
client = gspread.authorize(creds)

# opening the spreadsheet
sheet_id = "1Jc7roe2tmtVx-0hdn6DPI2zDh6NcPyWLBMVZN20a5WM"
sh = client.open_by_key(sheet_id)

#  defining color hex codes for formatting
Colors = {
    "bg" : [207 / 255.0, 226 / 255.0, 243 / 255.0],
    "Gray_1" : [183 / 255.0, 183 / 255.0, 183 / 255.0],
    "Gray_2" : [204 / 255.0, 204 / 255.0, 204 / 255.0],
    "Gray_3" : [217 / 255.0, 217 / 255.0, 217 / 255.0],
    "Purple_1" : [103 / 255.0, 78 / 255.0, 167 / 255.0],
    "Purple_2" : [142 / 255.0, 124 / 255.0, 195 / 255.0],
    "Purple_3" : [180 / 255.0, 167 / 255.0, 214 / 255.0],
    "Blue" : [61 / 255.0, 133 / 255.0, 198 / 255.0],
    "Black" : [0, 0, 0]
}

values_list = sh.sheet1.row_values(1)
# print(values_list)

# worksheet = sh.add_worksheet(title="Opeth", rows=500, cols=22)

# sh.opeth.update_tab_color({"red": 1, "green": 0.5, "blue": 0.5})

token = get_token()

artist = Artist(token, "Opeth")

worksheet = sh.worksheet(artist.artist_name)

# Inserting files based on position relative to other album lengths
# def format_album(range, alb):
#   return 1

# for alb in artist.album_objects:
#   format_album("A1B2", alb)


#                   Formatting non-album sections

# Setting background color & font for all cells
  
worksheet.format("A1:V500", {
    "backgroundColor": {
      "red": Colors["bg"][0],
      "green": Colors["bg"][1],
      "blue": Colors["bg"][2]
    },
    "horizontalAlignment": "CENTER",
    "verticalAlignment": "MIDDLE",
    "textFormat": {
      "fontFamily" : "Roboto Serif",
      "fontSize": 10,
    }
})

# Formatting Header

worksheet.format("B2:O4", {
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
      "fontFamily" : "Roboto Serif",
      "fontSize": 38,
      "bold": True
    }
})

worksheet.merge_cells("B2:O4")

worksheet.update_acell("B2", artist.artist_name)

# Formatting album rankings

worksheet.format("Q2:U4", {
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
      "fontFamily" : "Roboto Serif",
      "fontSize": 32,
      "bold": True
    }
})

worksheet.merge_cells("Q2:U4")

worksheet.update_acell("Q2", "Album Rankings")

worksheet.format("Q5:U5", {
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

worksheet.merge_cells("R5:T5")

worksheet.update_acell("Q5", "#")
worksheet.update_acell("R5", "Title")
worksheet.update_acell("U5", "Rating")

# Adding numbers / merging cells for albums to be put in rankings

for i in range (len(artist.album_objects)):
  worksheet.update_acell(f"Q{6 + i}", i + 1)
  worksheet.merge_cells(f"R{6 + i}:T{6 + i}")

time.sleep(100)

# Formatting song rankings

pos = 7 + len(artist.album_objects)

worksheet.format(f"Q{pos}:U{pos + 2}", {
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
      "fontFamily" : "Roboto Serif",
      "fontSize": 32,
      "bold": True
    }
})

worksheet.merge_cells(f"Q{pos}:U{pos + 2}")

worksheet.update_acell(f"Q{pos}", "Top 10 Songs")

worksheet.merge_cells(f"R{pos + 3}:T{pos + 3}")

worksheet.update_acell(f"Q{pos + 3}", "#")
worksheet.update_acell(f"R{pos + 3}", "Title")
worksheet.update_acell(f"U{pos + 3}", "Rating")

for i in range(10):
  worksheet.update_acell(f"Q{pos + 4 + i}", i + 1)
  worksheet.merge_cells(f"R{pos + 4 + i}:T{pos + 4 + i}")