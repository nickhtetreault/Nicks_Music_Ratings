import gspread

from gspread_formatting import *

from google.oauth2.service_account import Credentials

from artist_data import Artist, Album

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
worksheet = sh.worksheet("Opeth")

# worksheet.merge_cells("B2:O4", MergeType.merge_all)

worksheet.format("B2:O4", {
    "backgroundColor": {
      "red": Colors["Gray_1"][0],
      "green": Colors["Gray_1"][1],
      "blue": Colors["Gray_1"][2]
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
      "foregroundColor": {
        "red": Colors["Purple_1"][0],
        "green": Colors["Purple_1"][1],
        "blue": Colors["Purple_1"][2]
      },
      "fontSize": 12,
      "bold": True
    }
})