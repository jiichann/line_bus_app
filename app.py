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
            result = "".join(list)
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
            list = map(str, time.text)
            result = "".join(list)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= result))
    
    elif text == "入力":
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= "乗車するバス停を入力してください"))
        if text == "九大学研都市駅":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= "下車するバス停を入力してください"))
            start_number = "00291944"
            if text == "九大ビッグオレンジ":
                goal_number = "00087910"
                cur_url = "https://transfer.navitime.biz/showa-bus/extif/TransferSearchIF?startName=&goalName=&start=" + start_number + "&goal=" + goal_number + "&&device=pc"
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
                    result = "".join(list)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text= result))




       
# 元岡郵便局前：00291912
# 元岡小学校前：00291911
# 産学連携交流センター：00087909
# 九大中央図書館：00291995
# 九大イーストゾーン：00291994
# 九大東ゲート：00291993
# 九大理学部：00090936
# 九大工学部前：00087911
# 九大農学部：00291996
# 九大船舶・航空実験棟：00090773
# 九大総合グラウンド：00090774
# 伊都営業所：00291992
# 山崎（福岡県）：00291884
# 周船寺東口：00291883
# 周船寺：00291882
# 泉（福岡市）：00291947
# 富士見（福岡県）：00291948
# たろう保育園前：00291949
# 元岡農協前：00291950
# 九大伊都協奏館：00291957
# 桑原公民館：00291955
# 横浜西：00291946
# 工芸会ワークセンター：00291915
# 玄洋高校：00291914
# 今出（福岡県）：00291913