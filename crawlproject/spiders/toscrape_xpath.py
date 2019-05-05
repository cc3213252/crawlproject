# -*- coding: utf-8 -*-
import scrapy
from crawlproject.items import ToscrapeXpathItem


class ToscrapeXpathSpider(scrapy.Spider):
    name = 'toscrape_xpath'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            item = ToscrapeXpathItem()
            item['quote'] = quote.xpath('./span[@class="text"]/text()').extract_first()
            item['author'] = quote.xpath('.//small[@class="author"]/text()').extract_first()
            item['tags'] = quote.xpath('./div[@class="tags"]/a[@class="tag"]/text()').extract()
            author_page = response.xpath('.//small[@class="author"]/following-sibling::*/@href').extract_first()
            authro_full_url = response.urljoin(author_page)
            yield scrapy.Request(authro_full_url, meta={'item': item}, callback=self.parse_author, dont_filter=True)

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            next_full_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_full_url, callback=self.parse)

    def parse_author(self, response):
        item = response.meta['item']
        item['author_born_date'] = response.xpath('//span[@class="author-born-date"]/text()').extract_first()
        item['author_born_location'] = response.xpath('//span[@class="author-born-location"]/text()').extract_first()
        item['author_description'] = response.xpath('//div[@class="author-description"]/text()').extract_first()
        yield item

