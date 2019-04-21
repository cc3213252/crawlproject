# -*- coding: utf-8 -*-
import scrapy


class ZolSpider(scrapy.Spider):
    name = 'zol'
    allowed_domains = ['sj.zol.com.cn']
    start_urls = ['http://sj.zol.com.cn/bizhi/750x1334/']
    img_urls = []

    def parse(self, response):
        photos = response.xpath('//li[@class="photo-list-padding"]')
        for photo in photos:
            album_url = photo.xpath('./a/@href').get()
            title = photo.xpath('./a/@title').get()
            album_full_url = response.urljoin(album_url)
            self.logger.info(title)
            self.logger.info(album_full_url)
