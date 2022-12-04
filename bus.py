from time import sleep
from selenium import webdriver
import chromedriver_binary
import os
import signal
import requests
from bs4 import BeautifulSoup
import re
import datetime
import json
json_open = open('bus\linebot.json', 'r')

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import By


# try:

# Chromeを起動
options = Options()
# # ブラウザを開かない
# options.add_argument('--headless')
# # 画像非表示
# options.add_argument('--blink-settings=imagesEnabled=false')
# driver = webdriver.Chrome("chromedriver.exe", options=options)
# # 指定したURLに遷移する
# driver.get("http://showa-bus.jp/")

# print("出発")
# departure = input()

# def input_time(departure, arrival):
#     driver.find_element(By.ID, 'departure').send_keys(departure)
#     driver.find_element(By.ID, 'arrival').send_keys(arrival)

# if departure == "行く":
#     input_time("九大学研都市駅", "九大ビッグオレンジ")
# elif departure == "帰る":
#     input_time("九大ビッグオレンジ", "九大学研都市駅")
# else:
#     print("到着")
#     arrival = input()
#     input_time(departure, arrival)

# # 検索をクリック
# driver.find_element(By.ID, "search1").click()  

# # ウィンドウハンドルを取得する(list型配列)
# handle_array = driver.window_handles
#     # seleniumで操作可能なdriverを切り替える
# driver.switch_to.window(handle_array[-1])
#     #遷移後のURLを取得
# cur_url = driver.current_url

cur_url = "https://transfer.navitime.biz/showa-bus/extif/TransferSearchIF?startName=&goalName=&start=00291944&goal=00087910&device=pc"
# requetsを使ってサイト情報を取得
result = requests.get(cur_url)
# 日本語の文字化け防止
result.encoding = result.apparent_encoding
# 要素を解析
bs = BeautifulSoup(result.text, "html.parser")
for time in bs.find_all(class_ = "startGoalTime"):
    print(time.text)
    for eraser1 in bs.find_all(class_ = "start"):
        eraser1.clear()
    for eraser2 in bs.find_all(class_ = "goal"):
        eraser2.clear()
    
# 開いているWebブラウザを閉じる
# driver.quit()

# finally:
#     os.kill(driver.service.process.pid,signal.SIGTERM)