import scrapy
import datetime
import bookinfo.items as items


class bookinfo(scrapy.Spider):
    name = "bookinfo"
    #start_urls = ('http://www.yousuu.com/category/all',)
    start_urls = ('http://www.yousuu.com/book/1',)
    base_url = 'http://www.yousuu.com/book/'
    start = False

    def parse(self, response):
        selector = scrapy.Selector(response)

        if self.start:
            start = False

            latestBookID = selector.css("div.post a::attr(href)").extract()
            startFrom = self.base_url + latestBookID[0]
            yield scrapy.http.Request(startFrom, callback=self.parse)

        centralBlock = selector.css("div.center-block::text").extract()

        currUrl = response.request.url
        nextBookID = int(''.join(c for c in currUrl if c.isdigit())) - 1
        nextUrl = self.base_url + str(nextBookID)

        # center-block class exists, the url is invalid for book information
        if nextBookID < 0:
            return

        if centralBlock:
            yield scrapy.http.Request(nextUrl, callback=self.parse)
        else:
            # book tags
            tags = selector.css("div.sokk-book-buttons::attr(data-tags)").extract()

            # get the url of book avatar
            bookImage = selector.css("img.bookavatar::attr(src)").extract()[0]

            # get basic info of book
            bookName = selector.css("div.col-sm-7 div span::text").extract()[0]

            basicInfo = selector.css("ul.list-unstyled li::text").extract()
            # format:
            # ['作者:', '字数: 2962799字 ', '章节数: 351章 ',
            # '来自: 起点中文网', '更新时间: 09/03/05 00:07',
            # '最新章节: 第三十二集 尘埃落定 第六章 帝国新生（下）全书完']
            wordCount = basicInfo[1][4:]
            chapterCount = basicInfo[2][5:]
            sourceWebsite = basicInfo[3][4:]
            updateTime = basicInfo[4][6:]
            latestUpdate = basicInfo[5][6:]
            authorName = selector.css("ul.list-unstyled li a::text").extract()[0]

            summary = selector.css("div.panel-body::text").extract()[0]

            
            #yield scrapy.http.Request(nextUrl, callback=self.parse)









