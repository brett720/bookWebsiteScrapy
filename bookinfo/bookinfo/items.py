# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    wordCount = scrapy.Field()
    chapterCount = scrapy.Field()
    sourceWebsite = scrapy.Field()
    updateTime = scrapy.Field()
    latestUpdateChap = scrapy.Field()
    authorName = scrapy.Field()
    summary = scrapy.Field()
    tags = scrapy.Field()
    bookImage = scrapy.Field()
    bookName = scrapy.Field()
    bid = scrapy.Field()

    pass
