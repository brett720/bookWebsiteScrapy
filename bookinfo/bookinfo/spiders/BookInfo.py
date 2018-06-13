import scrapy
import datetime
import bookinfo.items as items


class bookinfo(scrapy.Spider):
    name = "bookinfo"
    #start_urls = ('http://www.yousuu.com/category/all',)
    start_urls = ('http://www.yousuu.com/book/145126',)
    base_url = 'http://www.yousuu.com/book/'
    start = False

    def parse(self, response):
        selector = scrapy.Selector(response)
        item = items.BookinfoItem()
        if self.start:
            self.start = False

            latestBookID = selector.css("div.post a::attr(href)").extract()
            startFrom = 'http://yousuu.com' + latestBookID[0]
            yield scrapy.http.Request(startFrom, callback=self.parse)

        else:
            centralBlock = selector.css("div.center-block::text").extract()

            currUrl = response.request.url
            currBookID = int(''.join(c for c in currUrl if c.isdigit()))
            nextUrl = self.base_url + str(currBookID - 1)

            # center-block class exists, the url is invalid for book information
            if currBookID < 1:
                return

            if centralBlock:
                yield scrapy.http.Request(nextUrl, callback=self.parse)
            else:
                # book id
                item['bid'] = str(currBookID)

                # book tags
                item['tags'] = selector.css("div.sokk-book-buttons::attr(data-tags)").extract()

                # get the url of book avatar
                item['bookImage'] = selector.css("img.bookavatar::attr(src)").extract()[0]

                # get basic info of book
                item['bookName'] = selector.css("div.col-sm-7 div span::text").extract()[0]

                basicInfo = selector.css("ul.list-unstyled li::text").extract()
                # format:
                # ['作者:', '字数: 2962799字 ', '章节数: 351章 ',
                # '来自: 起点中文网', '更新时间: 09/03/05 00:07',
                # '最新章节: 第三十二集 尘埃落定 第六章 帝国新生（下）全书完']
                item['wordCount'] = basicInfo[1][4:]
                item['chapterCount'] = basicInfo[2][5:]
                item['sourceWebsite'] = basicInfo[3][4:]
                item['updateTime'] = basicInfo[4][6:]
                item['latestUpdateChap'] = basicInfo[5][6:]

                # get author name.
                author = selector.css("ul.list-unstyled li a::text").extract()
                if not author:
                    authorName = author[0]
                else:
                    authorName = ''
                item['authorName'] = authorName

                # get summary
                summaryContent = selector.css("div.panel-body::text").extract()
                if not summaryContent:
                    summary = summaryContent[0]
                else:
                    summary = ''
                item['summary'] = summary

                yield (item)

                yield scrapy.http.Request(nextUrl, callback=self.parse)









