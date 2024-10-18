from flask import Flask, request, jsonify
import os

# Your Python script (import this if it's in a different file)
# import batch_formatting_sheet  # This should be the script that generates Google Spreadsheets
from batch_formatting_sheet import generate_spreadsheet
app = Flask(__name__)


# This route listens for POST requests
@app.route('/trigger', methods=['POST'])
def trigger_script():
    try:
        # Get the data sent from Google Apps Script (JSON payload)
        data = request.json

        # Assuming 'data' contains the cell and its value
        sheet_name = data.get('sheetName')
        cell = data.get('cell')
        value = data.get('value')

        # Log the received data
        print(f"Received data: Sheet: {sheet_name}, Cell: {cell}, Value: {value}")

        if value == "":
            raise Exception("No artist provided")

        print("I got here idk")
        generate_spreadsheet(value)

        # Respond back to the sender
        return jsonify({"status": "Script executed successfully"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on a specific port (5000 by default)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
