from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from db import get_weekly_total
import os
from dotenv import load_dotenv
import requests

# 環境変数読み込み
load_dotenv()
LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

def send_weekly_total():
    """ 今週の合計金額をLINEに送信 """
    total = get_weekly_total()
    message = f"今週の合計は {total}円です 🎉"

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, json=payload, headers=headers)

# スケジューラー設定
scheduler = BackgroundScheduler()
scheduler.add_job(send_weekly_total, "cron", day_of_week="sun", hour=20, minute=0)
scheduler.start()
