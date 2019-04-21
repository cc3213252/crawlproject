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
            yield scrapy.Request(album_full_url, meta={'title': title}, callback=self.parse_album, dont_filter=True)

    def parse_album(self, response):
        title = response.meta['title']
        img_url = response.xpath('//img[@id="bigImg"]/@src').get()
        self.img_urls.append(img_url)
        other_pics = response.xpath('//ul[@id="showImg"]/li')
        for item in other_pics:
            url = item.xpath('.//a/@href').get()
            pic_full_url = response.urljoin(url)
            yield scrapy.Request(pic_full_url, callback=self.parse_other_pic, dont_filter=True)

    def parse_other_pic(self, response):
        img_url = response.xpath('//img[@id="bigImg"]/@src').get()
        self.img_urls.append(img_url)
        self.logger.info(img_url)