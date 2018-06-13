# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

# open database
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb
books = db.books


# check if the bookId exists in db.books, return true.
def checkBookExist(bookId):
    if books.find({'bookId': bookId}).count() > 0:
        return True
    else:
        return False


# find the latest book id.
def findLastBookId():
    # overall url
    allCategoryUrl = "http://www.yousuu.com/category/all"
    pageData = requests.get(allCategoryUrl).text
    soup = BeautifulSoup(pageData, 'lxml')

    # get the latest bookid
    latest = soup.select_one("div[class=post]")
    bookLink = latest.contents[0].__str__()
    pattern = re.compile('\d+')
    lastBook = pattern.findall(bookLink)

    # return book id
    return int(lastBook[0])


# scrape book from latest book to the earliest,
# skip the book already in database.
def scrapeBook(start):
    # start url
    baseUrl = "http://www.yousuu.com/book/"
    for index in range(start, 0, -1):
        if index % 1000 == 0:
            print(index)

        #skip if book already in database
        if checkBookExist(index):
            print("read to ", str(index + 1))
            break

        # get the book link.
        currUrl = baseUrl + str(index)
        currPage = requests.get(currUrl).text
        soup = BeautifulSoup(currPage, 'lxml')
        address = soup.select_one("div[class=media]")

        # if link not exists, skip current
        if address is None:
            continue

        # get the book name and author
        aTag = address.find_all('a', href=True)
        name = soup.select_one("head > title")
        bookInfo = name.contents[0].__str__().replace(' ', '').split('-')

        # get the summary of book.
        bookSummary = soup.find("div", class_='panel-body', text=True)
        if bookSummary:
            textSummary = bookSummary.text
        else:
            textSummary = 'no summary'

        store in database
        books.insert({'bookId': index,
                      'bookName': bookInfo[0],
                      'author': bookInfo[1],
                      'bookLink': aTag[0]['href'],
                      'bookSummary': textSummary})


def main():
    lastId = findLastBookId()
    scrapeBook(lastId)
    pass


if __name__ == '__main__':
    main()
