from flask import Flask, request, jsonify
import requests
import csv
import io

app = Flask(__name__)

# CSV Linkin
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQLROqKmgKIOBhrZxSjVIeVSILets3Y2n-vsyRx_5ayCYlyWEpEQ5EwoA97CT5DBPQ_9UZULG4zx2H9/pub?gid=0&single=true&output=csv"
SECRET_KEY = "tasapi1234"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Eğer istek /roblox-rank'e gelirse
    if request.path == '/roblox-rank':
        auth = request.headers.get("Authorization")
        if auth != SECRET_KEY:
            return jsonify({"error": "Yetkisiz"}), 403

        user_id = request.args.get('userId')
        try:
            response = requests.get(SHEET_URL)
            f = io.StringIO(response.text)
            reader = csv.DictReader(f)
            
            for row in reader:
                if str(row['UserId']) == str(user_id):
                    return jsonify({"userId": user_id, "birim": row['Birim'], "rutbe": row['Rutbe']})
            
            return jsonify({"userId": user_id, "birim": "Sivil", "rutbe": "Aday"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    return jsonify({"message": "API çalışıyor"}), 200

if __name__ == '__main__':
    app.run()
