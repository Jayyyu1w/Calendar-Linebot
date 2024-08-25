from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import datetime
from llm_extract import get_LLM_response
from google_calendar import Google_Calendar

app = Flask(__name__)

with open("lineapi.txt", "r", encoding="utf-8") as f:
    LINEAPI = f.readline().strip()
    WEBHOOK = f.readline().strip()

# 設置Line Messaging API
line_bot_api = LineBotApi(LINEAPI)
handler = WebhookHandler(WEBHOOK)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_message = get_LLM_response(event.message.text)
    print(reply_message)
    print(type(reply_message["purpose"]))
    calendar = Google_Calendar()
    try:
        calendar.add_event(reply_message)
        reply = "日曆事件新增成功"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    except:
        reply = "日曆事件新增失敗"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


if __name__ == "__main__":
    app.run()