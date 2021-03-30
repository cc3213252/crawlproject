# -*- coding: utf-8 -*-
import scrapy
from crawlproject.items import ToscrapeXpathItem


class ToscrapeBetterSpider(scrapy.Spider):
    name = 'toscrape-better'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response, **kwargs):
        for quote in response.xpath('//div[@class="quote"]')[:1]:
            item = ToscrapeXpathItem()
            item['quote'] = quote.xpath('./span[@class="text"]/text()').get()
            item['author'] = quote.xpath('.//small[@class="author"]/text()').get()
            item['tags'] = quote.xpath('./div[@class="tags"]/a[@class="tag"]/text()').getall()
            author_page = quote.xpath('./span[2]/a')
            yield from response.follow_all(author_page,
                                           meta={'item': item},
                                           callback=self.parse_author,
                                           dont_filter=True)

        yield from response.follow_all(xpath='//li[@class="next"]/a', callback=self.parse)

    def parse_author(self, response):
        item = response.meta['item']
        item['author_born_date'] = response.xpath('//span[@class="author-born-date"]/text()').get()
        item['author_born_location'] = response.xpath('//span[@class="author-born-location"]/text()').get()
        item['author_description'] = response.xpath('//div[@class="author-description"]/text()').get()
        yield item

