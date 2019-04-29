# -*- coding: utf-8 -*-
import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['www.douban.com']
    start_urls = ['http://www.douban.com/']

    def start_requests(self):
        data = dict(
            ck='',
            name='username',
            password='password',
            remember='true',
            ticket='',
        )
        yield scrapy.FormRequest(url='https://accounts.douban.com/j/mobile/login/basic',
                                 formdata=data,
                                 callback=self.after_login)

    def after_login(self, response):
        self.logger.info(response)
        self.logger.info(response.text)