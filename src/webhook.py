from flask import Flask, request, jsonify
import os
from batch_formatting_sheet import *
from user_check_data import confirm_data
from artist_data import Artist

app = Flask(__name__)

@app.route('/trigger', methods=['POST'])
def trigger_script():
    try:
        # Get the data sent from Google Apps Script (JSON payload)
        data = request.json

        # Assuming 'data' contains the cell and its value
        sheet_name = data.get('sheetName')
        cell = data.get('cell')
        value = data.get('value')
        gid = data.get('id')

        # Log the received data
        print(f"Received data: Sheet: {sheet_name}, Cell: {cell}, Value: {value}, ID: {gid}")

        if value == "":
            raise Exception("No artist provided")
        elif value.lower() == "y":
            # right now this has me generating same artist twice, I want to try and avoid this but not sure how atm
            generate_spreadsheet(sheet_name)
        elif value.lower() == "n":
            delete_spreadsheet(sheet_name)
            raise Exception("Data not confirmed")
            # handle this case later in more detail
        else:
            # checking data if artist name provided
            target_id = confirm_data(value)
            linkArtistSheet(sheet_name, cell, value, target_id)
            

        # Respond back to the sender
        return jsonify({"status": "Script executed successfully"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
