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
    text = event.message.text
    if text == "九大学研都市駅→九大ビッグオレンジ":
        cur_url = "https://transfer.navitime.biz/showa-bus/extif/TransferSearchIF?startName=&goalName=&start=00291944&goal=00087910&device=pc"
        # requetsを使ってサイト情報を取得
        result = requests.get(cur_url)
        # 日本語の文字化け防止
        result.encoding = result.apparent_encoding
        # 要素を解析
        bs = BeautifulSoup(result.text, "html.parser")
        for time in bs.find_all(class_ = "startGoalTime"):
            for eraser1 in bs.find_all(class_ = "start"):
                eraser1.clear()
            for eraser2 in bs.find_all(class_ = "goal"):
                eraser2.clear()
            list = map(str, time.text)
            result = "\n".join(list)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= result))

    elif text == "九大ビッグオレンジ→九大学研都市駅":
        cur_url = "https://transfer.navitime.biz/showa-bus/extif/TransferSearchIF?startName=&goalName=&start=00087910&goal=00291944&&device=pc"
        # requetsを使ってサイト情報を取得
        result = requests.get(cur_url)
        # 日本語の文字化け防止
        result.encoding = result.apparent_encoding
        # 要素を解析
        bs = BeautifulSoup(result.text, "html.parser")
        for time in bs.find_all(class_ = "startGoalTime"):
            for eraser1 in bs.find_all(class_ = "start"):
                eraser1.clear()
            for eraser2 in bs.find_all(class_ = "goal"):
                eraser2.clear()
            list = map(str, time)
            result = "\n".join(list.text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= result))
    
    elif text == "入力":
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= "乗車するバス停を選択してください"))
        input(text = "入力してください")


        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= "下車するバス停を入力してください"))
        


    