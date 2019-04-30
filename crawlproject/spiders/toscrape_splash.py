# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class ToscrapeSplashSpider(scrapy.Spider):
    name = 'toscrape_splash'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args=dict(wait=0.5))

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            author = quote.xpath('.//small[@class="author"]/text()').get()
            self.logger.info('author: {}'.format(author))