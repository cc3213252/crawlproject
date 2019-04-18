# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ZolSpider(CrawlSpider):
    name = 'zol'
    allowed_domains = ['sj.zol.com.cn/bizhi']
    start_urls = ['http://sj.zol.com.cn/bizhi']
    img_urls = []
    rules = (
        Rule(LinkExtractor(allow=('/detail_8737_97214.html',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('//h1/a/text()').extract_first()
        img_url = response.xpath('//img[@id="bigImg"]/@src').extract_first()
        print(title)
        print(img_url)
