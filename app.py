from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from db import init_db, add_expense
import requests

# 環境変数読み込み
load_dotenv()
LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)
init_db()

def reply_message(reply_token, text):
    """ LINEへメッセージ送信 """
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, json=payload, headers=headers)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json

    for event in body["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            message = event["message"]["text"]
            reply_token = event["replyToken"]

            try:
                meal, price = message.split(" ")
                price = float(price)
                add_expense(meal, price)
                reply_message(reply_token, f"「{meal}」を{price}円で記録しました")
            except ValueError:
                reply_message(reply_token, "「食事 金額」の形式で送信してください")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
