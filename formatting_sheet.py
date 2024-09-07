import gspread

from google.oauth2.service_account import Credentials

# authorizing code to edit my spreadsheets with credentials (hidden)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes = scopes)
client = gspread.authorize(creds)

# opening the spreadsheet
sheet_id = "1Jc7roe2tmtVx-0hdn6DPI2zDh6NcPyWLBMVZN20a5WM"
sheet = client.open_by_key(sheet_id)

values_list = sheet.sheet1.row_values(1)
print(values_list)


# Formatting the google sheet with gspread and Google Sheets api