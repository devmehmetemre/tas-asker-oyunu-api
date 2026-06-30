from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

# Kopyaladığın o CSV linkini buraya yapıştır
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQLROqKmgKIOBhrZxSjVIeVSILets3Y2n-vsyRx_5ayCYlyWEpEQ5EwoA97CT5DBPQ_9UZULG4zx2H9/pub?gid=0&single=true&output=csv"
SECRET_KEY = "SeninGizliSifren123"

def get_rank_from_sheet(user_id):
    try:
        # Google Sheets'ten veriyi çek
        df = pd.read_csv(SHEET_URL)
        # UserId sütununu string'e çevir ki eşleşme hatası olmasın
        df['UserId'] = df['UserId'].astype(str)
        
        # Kullanıcıyı bul
        user_row = df[df['UserId'] == str(user_id)]
        
        if not user_row.empty:
            return {
                "birim": user_row.iloc[0]['Birim'],
                "rutbe": user_row.iloc[0]['Rutbe']
            }
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    return {"birim": "Sivil", "rutbe": "Aday"}

@app.route('/roblox-rank', methods=['GET'])
def get_rank():
    # Güvenlik Kontrolü
    auth = request.headers.get("Authorization")
    if auth != SECRET_KEY:
        return jsonify({"error": "Yetkisiz erişim"}), 403

    user_id = request.args.get('userId')
    data = get_rank_from_sheet(user_id)
    
    return jsonify({"userId": user_id, "birim": data["birim"], "rutbe": data["rutbe"]})

if __name__ == '__main__':
    app.run()