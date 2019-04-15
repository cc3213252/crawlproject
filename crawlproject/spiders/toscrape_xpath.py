# -*- coding: utf-8 -*-
import scrapy


class ToscrapeXpathSpider(scrapy.Spider):
    name = 'toscrape-xpath'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield dict(
                quote=quote.xpath('./span[@class="text"]/text()').extract_first(),
                author=quote.xpath('.//small[@class="author"]/text()').extract_first(),
                tags=quote.xpath('./div[@class="tags"]/a[@class="tag"]/text()').extract(),
            )

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            next_full_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_full_url, callback=self.parse)