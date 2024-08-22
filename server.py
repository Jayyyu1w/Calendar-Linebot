from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import datetime
from llm_extract import get_LLM_response
#import googleapiclient.discovery
#from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

with open("lineapi.txt", "r", encoding="utf-8") as f:
    LINEAPI = f.readline().strip()
    WEBHOOK = f.readline().strip()

# 設置Line Messaging API
line_bot_api = LineBotApi(LINEAPI)
handler = WebhookHandler(WEBHOOK)

# 設置Google日曆API
#SCOPES = ['https://www.googleapis.com/auth/calendar']
#SERVICE_ACCOUNT_FILE = 'path/to/your/service-account.json'

#credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
#service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

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
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run()