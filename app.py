from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

YOUR_CHANNEL_ACCESS_TOKEN = "VZAuJgMTkAG/U1IXO56PIFpq3slBd8yfd6bTIEh+liHNoxBLmv1TljelFGLZ+zzdJuf4Tnm7FkhiSNZEeMl/ZVvQr9ulx7BpIzkYYSas3p9XM3/W5hx9QzjkNubntilL5+1bBHSh8DwFTGr33EQPNQdB04t89/1O/w1cDnyilFU="


app = Flask(__name__)

line_bot_api = LineBotApi('VZAuJgMTkAG/U1IXO56PIFpq3slBd8yfd6bTIEh+liHNoxBLmv1TljelFGLZ+zzdJuf4Tnm7FkhiSNZEeMl/ZVvQr9ulx7BpIzkYYSas3p9XM3/W5hx9QzjkNubntilL5+1bBHSh8DwFTGr33EQPNQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('648ebf5005787f011e3cb5b3ba87cc80')


@app.route("/sample", methods=['GET'])
def sample():
    return "sample route desu"

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    options = Options()
    
    line_bot_api.reply_message(
        # event.reply_token,
        # TextSendMessage(text=event.message.text)
        TextSendMessage(text='Hello, world'))


# if __name__ == "__main__":
#  # app.run()
#     port = int(os.getenv("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
