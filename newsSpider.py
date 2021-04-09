import urllib.request
import datetime
import os
from bs4 import BeautifulSoup


# News物件 -------------------------------------------------
class News():
	def __init__(self,url):
		response = urllib.request.urlopen(url)
		self.soup = BeautifulSoup(response, "html.parser")
		self.date = self.dateToString(datetime.date.today())
		self.url = url
		self.source = self.getSource(url)
		self.title = ''
		self.article = ''
	def dateToString(self,date):
		monthDict = {
			"01":"Jan.",
			"02":"Feb.",
			"03":"Mar.",
			"04":"Apr.",
			"05":"May",
			"06":"Jun.",
			"07":"Jul.",
			"08":"Aug.",
			"09":"Sep.",
			"10":"Oct.",
			"11":"Nov.",
			"12":"Dec.",
		}
		dateArr = str(date).split("-")
		dateArr[1] = monthDict.get(dateArr[1],'None')
		dateString = f"{dateArr[1]} {dateArr[2]}, {dateArr[0]}"
		return dateString
	def getData(self):	
		link = f"link:'{self.url}',\n"
		title = f"title:'{self.title}',\n"
		content = f"content:{self.content},\n"
		source = f"source:'{self.source}',\n"
		date = f"date:'{self.date}',\n"
		photos = f"photos:{self.photos}"
		return link + title + content + source + date + photos
	def getSource(self,url):
		sourceArr = url.split('/')
		source = sourceDict[sourceArr[2]]
		return source
	def createHTML(self):
		top = open("data/top.txt",'r',encoding="utf-8")
		bottom = open("data/bottom.txt",'r',encoding="utf-8")
		result = top.read() + self.getData() + bottom.read()
		path = f'C:\\Users\Asus\Desktop\E-News\{self.date}'
		if not os.path.isdir(path):
			os.makedirs(path)
		html = open (f"{path}\{self.title}.html","w",encoding="utf-8")
		html.write(result)
		html.close()


# NewsType爬蟲 --------------------------------

class LineNews(News):
  def __init__(self,url):
			super().__init__(url)
			self.title = self.soup.find("h1",class_="entityTitle").getText().strip()
			self.content = []
			self.photos = []
			article = self.soup.find('article')
			for index,item in enumerate(article,start=0):
				if item.find('img'):
					self.content.append('')
					src = item.find('img').get("data-src")
					remark = item.find("figcaption").getText()
					photo = {
						"src":src,
            "index":index,
            "remark":remark,
            "style":{'margin':"auto"}
					}
					self.photos.append(photo)
				else :
					if item.find('a'):
						continue
					elif item.find("b"):
						self.content.append("!!"+item.getText())
					else :
						self.content.append(item.getText())


class undMoneyNews(News):
  def __init__(self,url):
			super().__init__(url)
			self.title = self.soup.find("h2",id="story_art_title").getText().strip()
			self.content = []
			self.photos = []
			article = self.soup.find('div',id="article_body")
			for index,item in enumerate(article,start=0):
				if item.find('img') != -1 and item.find('img') != None:
					self.content.append('')
					src = item.find('img').get("src")
					remark = item.find("figcaption").getText()
					photo = {
						"src":src,
            "index":index,
            "remark":remark,
            "style":{'margin':"auto"}
					}
					self.photos.append(photo)
				else :
					if item.find('a'):
						continue
					elif item.find("b"):
						self.content.append("!!"+item.getText())
					else :
						self.content.append(item.getText())


# 執行 --------------------------------------
sourceDict = {
  "today.line.me":"LINE Today",
  "money.udn.com":"經濟日報"
}

def createNews(source,url):
  news = News
  if(source == "today.line.me"):
    news=LineNews(url)
  elif(source == "money.udn.com"):
    news=undMoneyNews(url)
  news.createHTML()


def autoCreate():
	newsUrl = open("news.txt",'r',encoding="utf-8")
	for news in newsUrl:
		for source in sourceDict:
			if(source in news):
				createNews(source,news.strip())

autoCreate()

