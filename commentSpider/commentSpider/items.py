# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    username = scrapy.Field()
    uid = scrapy.Field()
    rating = scrapy.Field()
    currTime = scrapy.Field()
    postTime = scrapy.Field()
    cid = scrapy.Field()
    commentList = scrapy.Field()
    bookID = scrapy.Field()
