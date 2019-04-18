# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from crawlproject.misc.store import quotesbotDB


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = codecs.open('toscrape.js', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class ToscrapeXpathPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "toscrape-xpath":
            if item.get("quote", None) is None: return item
            spec = { "quote": item["quote"] }
            quotesbotDB.quotedb.update(spec, {'$set': dict(item)}, upsert=True)