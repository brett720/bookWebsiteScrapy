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

client = MongoClient('mongodb://localhost:27017/')
db = client.mydb
books = db.books

# books.remove({"bookId": "0"})
# books.insert(testBook)


def checkBookExist(bookId):
    if books.find({'bookId': bookId}).count() > 0:
        return True
    else:
        return False


for index in range(int(lastBook[0]), 0, -1):
    if index % 1000 == 0:
        print(index)

    if checkBookExist(index):
        print(index, "not exists in database.")
        continue

    currUrl = baseUrl + str(index)
    currPage = requests.get(currUrl).text

    soup = BeautifulSoup(currPage, 'lxml')

    address = soup.select_one("div[class=media]")
    if address is None:
        print(index, "not exits in yousuu.")
        continue
    aTag = address.find_all('a', href=True)
    # print(aTag[0]['href'])

    name = soup.select_one("head > title")
    bookInfo = name.contents[0].__str__().replace(' ', '').split('-')
    # print(bookInfo)

    books.insert({'bookId': index,
                  'bookName': bookInfo[0],
                  'author': bookInfo[1],
                  'bookLink': aTag[0]['href']})





