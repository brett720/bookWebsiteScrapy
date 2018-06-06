# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class CommentspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('comments.json', 'a', 'utf8')


    def process_item(self, item, spider):

        username = item['username']
        uid = item['uid']
        rating = item['rating']
        currTime = item['currTime']
        postTime = item['postTime']
        cid = item['cid']
        commentList = item['commentList']
        bookID = item['bookID']

        for index in range(len(username)):
            book = {}
            book['username'] = username[index]
            book['uid'] = uid[index]
            book['rating'] = rating[index]
            book['cid'] = cid[index]
            book['commentList'] = commentList[index]
            book['bookID'] = bookID[index]

            book['currTime'] = currTime[index]
            book['postTime'] = postTime[index]

            curr = json.dumps(dict(book), ensure_ascii=False) + '\n'
            self.file.write(curr)

        return item
