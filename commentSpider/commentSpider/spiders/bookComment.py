# -*- coding: utf-8 -*-
import scrapy
import datetime
import commentSpider.items as itemClass

class CommentSpider(scrapy.Spider):
    name = "bookComment"

    start_urls = ('http://www.yousuu.com/comments',)

    def parse(self, response):
        selector = scrapy.Selector(response)
        item = itemClass.CommentSpiderItem()
        # read the link of next page button
        baseUrl = 'http://www.yousuu.com/comments?t='
        pageInfo = selector.css("ul.pagination li a::attr(onclick)").extract()[1]

        # pageInfo sample: ys.common.jumpurl('t','1527969899')
        pageId = ''.join(c for c in pageInfo if c.isdigit())


        # collect uid of comments in current page
        userLink = selector.css("div.ys-comments-main a::attr(href)").extract()
        uid = []
        index = 0
        for each in userLink:
            if 'comments' in each and index % 2 == 0:
                uid.append(''.join(num for num in each if num.isdigit()))
            index += 1

        # get cid from comments
        cid = selector.css("div::attr(data-cid)").extract()

        # get username
        username = selector.css("h5.media-heading a::text").extract()

        # get rating of books
        rating = selector.css("span.num2star::text").extract()

        # get book id
        bookLink = selector.css("div.ys-comments-message small a::attr(href)").extract()
        bookID = []
        for book in bookLink:
            bookID.append(''.join(c for c in book if c.isdigit()))


        # get time string and curr time.
        postTime = []
        currTimeList = []
        timeList = selector.css("h5.media-heading small::text").extract()
        for s in timeList:
            s = s.replace("\n", "")
            timeStrList = s.split(" ")
            post = timeStrList[1] + timeStrList[2]
            postTime.append(post)

        currTime = datetime.datetime.now().__str__()
        currTimeList = [currTime] * 40


        # get comments text
        commentList = []
        rawComment = selector.css("div.ys-comments-message ::text").extract()
        currComment = ""
        index = 0
        while index < len(rawComment):
            if '(本书评来自于' in rawComment[index]:
                commentList.append(currComment[2:])
                currComment = ""
                index += 3

            else:
                currComment += rawComment[index]
                index += 1

        item['username'] = username
        item['uid'] = uid
        item['rating'] = rating
        item['currTime'] = currTimeList
        item['postTime'] = postTime
        item['cid'] = cid
        item['commentList'] = commentList
        item['bookID'] = bookID

        yield(item)

        if pageInfo:
            nextPageUrl = baseUrl + pageId
            yield scrapy.http.Request(nextPageUrl, callback=self.parse)