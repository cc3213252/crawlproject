# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from crawlproject.misc.store import quotesbotDB
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re


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


class FengniaoPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename = '{}.jpg'.format(item['title'])
        return filename

    def get_media_requests(self, item, info):
        yield Request(item['img_url'], meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item