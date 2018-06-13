# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class BookinfoPipeline(object):
    def __init__(self):
        self.file = codecs.open('bookInfo.json', 'a', 'utf8')

    def process_item(self, item, spider):

        book = dict(item)

        curr = json.dumps(book, ensure_ascii=False) + '\n'
        self.file.write(curr)


        return item
