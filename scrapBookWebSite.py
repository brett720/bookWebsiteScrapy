import requests
import re
from bs4 import BeautifulSoup

# get the latest book id
allCategoryUrl = "http://www.yousuu.com/category/all"
pageData = requests.get(allCategoryUrl).text
soup = BeautifulSoup(pageData, 'lxml')

latest = soup.select_one("div[class=post]")
address = latest.contents[0].__str__()
pattern = re.compile(r'\d+')
bookId = pattern.findall(address)
print(bookId[0])



