import requests
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

# get the latest book id
allCategoryUrl = "http://www.yousuu.com/category/all"
pageData = requests.get(allCategoryUrl).text
soup = BeautifulSoup(pageData, 'lxml')

latest = soup.select_one("div[class=post]")
address = latest.contents[0].__str__()
pattern = re.compile('\d+')
lastBook = pattern.findall(address)


# get all id with official website and store in MongoDB
baseUrl = "http://www.yousuu.com/book/"

client = MongoClient('localhost', 27017)
db = client.books

testBook = {"bookId" : 0,
             "bookName" : "测试"}

db.books.insert_one(testBook)




