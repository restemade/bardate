
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_FILE = "date.json"
TG_TOKEN = "8132090842:AAE3z3SNMV2z8V4ord_YE7zfo0uPLrL86lo"
TG_CHAT_ID = "@humbleloungee"

def send_telegram(order):
    items = "\n".join([f"- {item['name']} ({item['price']} ₸)" for item in order['cart']])
    text = f"📥 Новый заказ от {order['user']}\n" \
           f"🕒 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n" \
           f"{items}\n" \
           f"💰 Итого: {order['total']} ₸"
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"⚠️ Ошибка Telegram: {e}")

@app.route("/save", methods=["POST"])
def save_order():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    data["saved_at"] = datetime.now().isoformat()

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(DATA_FILE, "r+", encoding="utf-8") as f:
        history = json.load(f)
        history.append(data)
        f.seek(0)
        json.dump(history, f, ensure_ascii=False, indent=2)

    send_telegram(data)

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(port=5000)
