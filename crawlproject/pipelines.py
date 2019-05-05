# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re
import pymongo


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = codecs.open('toscrape.js', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()


class ZolPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        print('item:', item)
        folder = item['title']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'{0}/{1}'.format(folder_strip, image_guid)
        print('file:', filename)
        return filename

    def get_media_requests(self, item, info):
        print('3333:', item)
        for img_url in item['img_urls']:
            yield Request(img_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path

