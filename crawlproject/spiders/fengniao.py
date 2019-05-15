# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlproject.items import FengniaoItem


class FengniaoSpider(CrawlSpider):
    name = 'fengniao'
    allowed_domains = ['photo.fengniao.com']
    start_urls = ['http://photo.fengniao.com/']

    rules = (
        Rule(LinkExtractor(allow=r'https://photo.fengniao.com/pic_\d{1,8}.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = FengniaoItem()
        item['title'] = response.xpath('//h3[@class="title overOneTxt"]/text()').get()
        item['img_url'] = response.xpath('//div[@class="imgBig"]/img/@src').get()
        return item
