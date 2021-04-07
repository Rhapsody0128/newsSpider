import requests
import datetime

from bs4 import BeautifulSoup

News = [
	"https://today.line.me/tw/v2/article/yKlaPG?utm_source=lineshare",
	"https://today.line.me/tw/v2/article/pxYeP7?utm_source=lineshare",
]

sourceDict = {
	"today.line.me":"LINE Today",
}


# for index,perNews in enumerate(News,start=1):
#   for i in range(len(sourceDict)):
# 		if sourceDict[i] in perNews:
# 			print("aasd")
  		





# News物件 -------------------------------------------------
class News():
	def __init__(self,url):
		response = requests.get(url)
		self.soup = BeautifulSoup(response.text, "html.parser")
		self.date = self.dateToString(datetime.date.today())
		self.url = url
		self.source = self.getSource(url)

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

	def getSource(self,url):
		sourceArr = url.split('/')
		source = sourceDict[sourceArr[2]]
		return source


class LineNews(News):
  def __init__(self,url):
			super().__init__(url)
			self.title = self.soup.find("h1").text
			self.article = self.soup.find('article')


a = LineNews("https://today.line.me/tw/v2/article/pxYeP7?utm_source=lineshare")
print(a.source)


# def buildNews(title,link,source,article):
# 	contnet = title.prettify()  #輸出排版後的HTML內容	

# 	print(contnet)
# 	html = open("test.html",'w',encoding="utf-8")	
# 	html.write(contnet)
# 	html.close()
z = open("test.txt",'w')
z.write("asdsadsad")