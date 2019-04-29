# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class ToscrapeLoginSpider(scrapy.Spider):
    name = 'toscrape-login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):
        yield scrapy.Request('http://quotes.toscrape.com/login', callback=self.before_login)

    def before_login(self, response):
        token = response.xpath('//input[@name="csrf_token"]/@value').get()
        self.logger.info('token: %s', token)
        return FormRequest.from_response(response,
                                         formdata=dict(
                                             csrf_token=token,
                                             password='admin',
                                             username='admin',
                                         ),
                                         callback=self.after_login)

    def after_login(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            goodreads_page = quote.xpath('.//small[@class="author"]/following-sibling::a[2]/@href').get()
            self.logger.info('goodreads_page: %s', goodreads_page)
