from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import os
import datetime
from llm_extract import get_LLM_response
from google_calendar import Google_Calendar

app = Flask(__name__)

with open("lineapi.txt", "r", encoding="utf-8") as f:
    LINEAPI = f.readline().strip()
    WEBHOOK = f.readline().strip()

# 設置Line Messaging API
configuration = Configuration(access_token=LINEAPI)
handler = WebhookHandler(WEBHOOK)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
    reply_message = get_LLM_response(event.message.text)
    print(reply_message)
    print(type(reply_message["purpose"]))
    calendar = Google_Calendar()
    try:
        calendar.add_event(reply_message)
        reply = "日曆事件新增成功"
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)])
        )
    except:
        reply = "日曆事件新增失敗"
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)])
        )


if __name__ == "__main__":
    app.run()