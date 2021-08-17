import requests
import os
from bs4 import BeautifulSoup

# index = 1
# response = requests.get(f"https://matrixmedia.crmls.org/mediaserver/GetMedia.ashx?Key=358550348&TableID=50&Type=1&Size=8&exk=857b7e83c4d970a0e5850909c8e6ebd5&Number={index}")

# soup = BeautifulSoup(response.text, "lxml")

# results = soup.find("img")

src = str(input('網址:'))
number = int(input('幾張:'))

for index in range(number):
  link = src + str(index)
  img = requests.get(link)
  with open("images\\" + str(index) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
    file.write(img.content)  # 