# -*- coding: utf-8 -*-

import json
class UserPipeline(object):
    """
    Save as a json file

    """
    def open_spider(self, spider):
        self.file = open('items.json', 'w',encoding="utf8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

import pymongo
class MongoPipeline(object):
    """
    This pipeline is not added to settings.py
    Save to mongodb
    """
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db["user"].update({"url_token":item["url_token"]},{"$set":item},True)
        return item