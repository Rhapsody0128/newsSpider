import urllib.request
import datetime
import os
from bs4 import BeautifulSoup


# News物件 -------------------------------------------------
class News():
	def __init__(self,url):
		self.date = self.dateToString(datetime.date.today())
		self.url = url
		self.source = self.getSource(url)
		self.title = None
		self.article = None
		self.soup = None
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
			response = urllib.request.urlopen(url)
			self.soup = BeautifulSoup(response, "html.parser")
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
			headers = {
			  # 假装自己是瀏覽器
			  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36',
			  # 把Cookie塞進来
			  'Cookie': "_ss_pp_id=0f44adb3ad15c57b76c1604962596976; _fbp=fb.1.1605233179886.1835971436; __auc=f4bc3b5c1761bfed62761ee46cc; __eruid=bbd8d64c-7c7f-a992-dd07-2ed02a382099; __BWfp=c1606787456246xc9fe0cdcd; dable_uid=91635153.1604991396416; _col_uuid=3380b9c7-5336-412e-87b9-13f832c9e39c-1sj20; _fbc=fb.1.1609295908859.IwAR008ibqthN4rRghbls8EFOzMXeDypV84MRjlGh-c-2OmBaYJxnaahAEreE; __erEvntUid=spgOKaGiN3C; ucfunnel_uid=35c0e90a-796c-3831-b601-b2486d0caceb; __retuid=ecb5800f-57b3-39a8-64f3-a764178a7421; __utma=30630269.1819547398.1605233180.1610943030.1610943030.1; __utmz=30630269.1610943030.1.1.utmgclid=Cj0KCQiA3Y-ABhCnARIsAKYDH7tN_JRQfPNVKacIgI7rTeVf0D1t9Rcz4iB1Dt2QYwylCfKQDD1BGK8aArU9EALw_wcB|utmccn=(not%20set)|utmcmd=(not%20set); _gcl_au=1.1.1890931655.1610943031; AviviD_uuid=8c332b62-48f8-43d1-9dca-c7f0b4b54f40; AviviD_refresh_uuid_status=1; webuserid=e00045a9-66d2-8a67-3540-6b93c13c6b09; AviviD_waterfall_status=1; __lastv=0; _gac_UA-65075410-1=1.1614665623.Cj0KCQiAvvKBBhCXARIsACTePW9YDP0cT47Lj35B2O8mLfSQV43XUqKvgevwvoia2QeKPKsHLZSrJC0aAtp-EALw_wcB; _ga_PSD1C9FJ2H=GS1.1.1614665622.3.0.1614665622.60; _gcl_aw=GCL.1614665623.Cj0KCQiAvvKBBhCXARIsACTePW9YDP0cT47Lj35B2O8mLfSQV43XUqKvgevwvoia2QeKPKsHLZSrJC0aAtp-EALw_wcB; _gac_UA-19660006-1=1.1614665623.Cj0KCQiAvvKBBhCXARIsACTePW9YDP0cT47Lj35B2O8mLfSQV43XUqKvgevwvoia2QeKPKsHLZSrJC0aAtp-EALw_wcB; _gac_UA-34729421-1=1.1614665623.Cj0KCQiAvvKBBhCXARIsACTePW9YDP0cT47Lj35B2O8mLfSQV43XUqKvgevwvoia2QeKPKsHLZSrJC0aAtp-EALw_wcB; __htid=9cb8abeb-60c4-4eac-8b0f-3ccc416d5a91; CFFPCKUUID=5711-JYSufI1PNPOwsxnFsMzdNvU9nR0ptop7; cto_bundle=I1wKF19la0JJNDkybEN0JTJCeVhJQk5VSmJOMm10YjB2MVpjUjlmUmt4eXl2bVNxJTJGeDJiY3E0dWZvVmNMRSUyQkNJbDhvSVVLQTlOSjhCYVFnNDZwWDRkbUt1RER5U1o5T0E1QUklMkZlT1lndXRNJTJGRGlGcXVxQVA0SFpYWU5BWjUwWVllZlNpNlRab05vbUM0ZmFwaVNPa1lMOW5WbFlBJTNEJTNE; _ga_GLZLGGK8BJ=GS1.1.1616638584.1.0.1616638589.0; _ga=GA1.2.1819547398.1605233180; _hjid=541ecc76-ba8d-467d-93d6-2219b10bde8a; _gid=GA1.2.1940541638.1618191760; csrf_cookie_name=5cb1a9bac98179395187716ce5e4d81a; _td=0c88b16e-14a1-4590-b16b-d47dc850293b; meter_1=1; meter_7=1; __gads=ID=b48af2af32d94819:T=1618200126:S=ALNI_MbU0f6kUVsPiRnsFRczrrYezqoPWA; __asc=d10f011b178c477744de50d9cdb; UdnCasId=HGGEkMxYBduYb4xhOrFsKA9c; TGT=TGT-5100-Fkdksvslw1q6Zz3dlbnarMlDoS9cGMNC5eBugR1Y9rDaxbhHRg-cas; udnmember=spgOKaGiN3C; um2=43d%2F0d%22%21%22%250%2B%22d0b%22%2233%2234%233%2B303%2B3c343%2F30343132333d30%21%21%3D%3D; udnemail=43d%2F0d2%2F43d%2F0d0c0%210%24020b0%220d430%24d202d%22030%210%23%21%21%3D%3D; membercenter=43d%2F0d%22%21%22%250%2B%22d0b%22%2233%223%21%3D; udnland=spgOKaGiN3C; udngold=43d%2F0d%22%21%22%250%2B%22d0b%22%2233%2234%233%2B303%2B3c343%2F30343132333d30%21%21%3D%3D; services=34333%2F3%2F3%2B4%24343%2F3%2F3%2F%21%21%3D%3D; isMoneyMember=Y; isMoneyMemberCheck=1b%21%21%3D%3D; login_status=true; disArtId=5381148; paywall_url=https%3A%2F%2Fmoney.udn.com%2Fmoney%2Fstory%2F12972%2F5381148; _gat_UA-19210365-3=1; _gat_UA-19660006-1=1",
			}
			session = urllib.requests.Session()
			response = session.get(url, headers=headers)
			self.soup = BeautifulSoup(response, "html.parser")
			self.title = self.soup.find("h2",id="story_art_title").getText().strip()
			self.content = []
			self.photos = []
			article = self.soup.find('div',id="article_body")
			print(article)
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
						print('zz')
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

