# -*- coding: utf-8 -*-
import scrapy
from crawlproject.items import ZolItem


class ZolSpider(scrapy.Spider):
    name = 'zol'
    allowed_domains = ['sj.zol.com.cn']
    start_urls = ['http://sj.zol.com.cn/bizhi/750x1334/']

    def parse(self, response):
        photos = response.xpath('//li[@class="photo-list-padding"]')
        for photo in photos[:1]:
            album_url = photo.xpath('./a/@href').get()
            title = photo.xpath('./a/@title').get()
            album_full_url = response.urljoin(album_url)
            yield scrapy.Request(album_full_url, meta={'title': title}, callback=self.parse_album)

    def parse_album(self, response):
        title = response.meta['title']
        item = ZolItem()
        item['title'] = title
        img_url = response.xpath('//img[@id="bigImg"]/@src').get()
        item['img_urls'] = [img_url]
        other_pics = response.xpath('//ul[@id="showImg"]/li')
        for other in other_pics:
            url = other.xpath('.//a/@href').get()
            pic_full_url = response.urljoin(url)
            self.logger.info(pic_full_url)
            yield scrapy.Request(pic_full_url, meta={'item': item}, callback=self.parse_other_pic)

    def parse_other_pic(self, response):
        item = response.meta['item']
        img_url = response.xpath('//img[@id="bigImg"]/@src').get()
        item['img_urls'].append(img_url)
        yield item