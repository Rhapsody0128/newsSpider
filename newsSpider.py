import urllib.request
import urllib.parse
import requests
import datetime
import os
from bs4 import BeautifulSoup

import re

# News物件 -------------------------------------------------


class News():
	def __init__(self,url):
		self.date = system.date
		self.url = url
		self.source = self.getSource(url)
		self.title = None
		self.article = None
		self.soup = None

	def removePunctuation(self,word):
		replaceWord = ''
		for char in word: 
			replaceChar = re.sub('/', '.', char) 
			replaceWord += replaceChar
		return replaceWord

	def getData(self):
		link = f"link:'{self.url}',\n"
		title = f"title:'{self.title}',\n"
		content = f"content:{self.content},\n"
		source = f"source:'{self.source}',\n"
		date = f"date:'{self.date}',\n"
		photos = f"photos:{self.photos}"
		return link + title + content + source + date + photos

	def getSource(self,url):
		if (url in'http'):
			sourceArr = url.split('/')
			for source in system.sourceDict :
				if (source in sourceArr[2]):
					return system.sourceDict[source]
		else :
			return url

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

	def createTXT(self):
		top = open("data/top.txt",'r',encoding="utf-8")
		bottom = open("data/bottom.txt",'r',encoding="utf-8")
		result = top.read() + self.getData() + bottom.read()
		path = f'C:\\Users\Asus\Desktop\E-News\{self.date}'
		if not os.path.isdir(path):
			os.makedirs(path)
		html = open (f"{path}\{self.title}.txt","w",encoding="utf-8")
		html.write(result)
		html.close()


# NewsType爬蟲 --------------------------------

class LineNews(News):
  def __init__(self,url):
			super().__init__(url)
			response = requests.get(url)
			self.soup = BeautifulSoup(response.text, "html.parser")
			self.title = self.removePunctuation(self.soup.find("h1",class_="entityTitle").getText().strip())
			self.content = []
			self.photos = []
			article = self.soup.find('article')
			for item in article:
				if item.find('img'):
					self.content.append('')
					src = item.find('img').get("data-src")
					remark = item.find("figcaption").getText()
					photo = {
						"src":src,
            "index":article.index(item),
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
			headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
			response = requests.get(url,headers=headers)
			self.soup = BeautifulSoup(response.text, "html.parser")

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
				else:
					if item.find('a'):
						continue
					elif item.find("b"):
						self.content.append("!!"+item.getText())
					else :
						self.content.append(item.getText())


class chinaTimesNews(News):
  def __init__(self,url):
			super().__init__(url)
			response = requests.get(url)
			self.soup = BeautifulSoup(response.text, "html.parser")
			self.title = self.soup.find("h1",class_="article-title").getText().strip()
			
			self.content = []
			self.photos = []

			topPhoto = self.soup.find("figure")
			if topPhoto != None :
				photo = topPhoto.find("img")
				self.content.append('')
				src = photo.get("src")
				remark = photo.parent.parent.find("figcaption").getText()
				photo = {
					"src":src,
          "index":0,
          "remark":remark,
          "style":{'margin':"auto"}
				}
				self.photos.append(photo)
			article = self.soup.find('div',class_='article-body')
			for item in article:
				if item.find('a'):
					continue
				elif item.find("b"):
					self.content.append("!!"+item.getText())
				else :
					self.content.append(item.getText())


class commercialNews(News):
  def __init__(self,url):
			super().__init__(url)
			response = requests.get(url)
			self.soup = BeautifulSoup(response.text, "html.parser")
			self.title = self.soup.find("span",class_="post-title").getText().strip()
			
			self.content = []
			self.photos = []

			topPhoto = self.soup.find('figure')

			if topPhoto != None :
				photo = topPhoto.find("img")
				self.content.append('')
				src = photo.get("data-src")
				remark = photo.parent.parent.find("figcaption").getText()
				photo = {
					"src":src,
          "index":0,
          "remark":remark,
          "style":{'margin':"auto"}
				}
				self.photos.append(photo)
			article = self.soup.find('div',class_='entry-content')
			for item in article:
				if item.find('figure'):
					photo = item.find("img")
					self.content.append('')
					if photo != -1 :
						src = photo.get("src")
						remark = photo.parent.parent.find("figcaption")
						if(remark != -1 and remark != None):
							remark = remark.getText()
						else:
							remark = ''
						photo = {
							"src":src,
							"index":article.index(item),
							"remark":remark,
							"style":{'margin':"auto"}
						}
						self.photos.append(photo)
				if item.find('a'):
					continue
				elif item.find('strong'):
					continue
				elif item.name == "h3":
					self.content.append("!!"+item.getText())
				else :
					self.content.append(item.getText())



# 執行 --------------------------------------

class System():
	def __init__(self):
		self.sourceDict = {
			"today.line.me":"LINE Today",
			"money.udn.com":"經濟日報",
			"www.chinatimes.com":"中時新聞網",
			"ctee.com.tw":"工商時報"
		}
		self.allTitle = []
		self.allUrl = []
		self.date=datetime.date.today().strftime("%b. %d, %Y")

	def createNews(self,source,url):
		news = News
		if(source == "today.line.me"):
			news=LineNews(url)
		elif(source == "money.udn.com"):
			news=undMoneyNews(url)
		elif(source == "www.chinatimes.com"):
			news=chinaTimesNews(url)
		elif(source == "ctee.com.tw"):
			news=commercialNews(url)
		news.createHTML()
		news.createTXT()
		self.allUrl.append(input(f"{news.title}\n所對應的網址是?"))
		self.allTitle.append(news.title)
		

	def createTypeHTML(self):
		top = open("data/typeTop.txt",'r',encoding="utf-8")
		bottom = open("data/typeBottom.txt",'r',encoding="utf-8")
		data = f"title:{self.allTitle},\nlink:{self.allUrl}"
		result = top.read() + data + bottom.read()
		path = f'C:\\Users\Asus\Desktop\E-News\{self.date}'
		if not os.path.isdir(path):
			os.makedirs(path)
		name = 'typeSetting'
		html = open (f"{path}\{name}.html","w",encoding="utf-8")
		html.write(result)
		html.close()

	def autoCreate(self):
		newsUrl = open("news.txt",'r',encoding="utf-8")
		for news in newsUrl:
			for source in self.sourceDict:
				if(source in news):
					self.createNews(source,news.strip())
		self.createTypeHTML()
		print('已完成')

system = System()
system.autoCreate()

