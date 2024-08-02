from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import datetime
#import googleapiclient.discovery
#from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 設置Line Messaging API
line_bot_api = LineBotApi('BVDQTC+Z8g/VMZu2D4muoukqjY73hEHN1KQFSX4pq9SSseacwGbUds0gDAsxyqFq/80AS7m/eZNjbFb9Vo2kgJV5bcy5AS+XF7iBzF4CzgUfkWQsh2BYdpVYmXuokrn79B4Si7/F0SUUW1CC3oNPVQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('eb550add503a9821b8f5bae35ab3faba')

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
    reply_message = "收到您的消息：" + event.message.text
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run()