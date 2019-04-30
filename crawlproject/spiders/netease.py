# -*- coding: utf-8 -*-
import scrapy
import demjson


class NeteaseSpider(scrapy.Spider):
    name = 'netease'
    allowed_domains = ['c.m.163.com']
    start_urls = ['http://c.m.163.com/dlist/article/dynamic?from=T1467284926140&offset=0&size=20&fn=1&LastStdTime=0&passport=&devId=oRVplVb3z7mN6qAtWNnhZw%3D%3D&lat=&lon=&version=32.1&net=wifi&ts=1556607862&sign=YR2UwmtOmCqPvhT2dFjbhLi7GpH%2BVMsRS3Fi5EESwSV48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=news_lf_cpa_2&mac=cV1UUJjt%2F0otjChfTgVYmXbpt7PSWbUoS%2FM7z6UHeeU%3D&open=&openpath=']

    def parse(self, response):
        content = demjson.decode(response.text)
        items = content['T1467284926140']
        for item in items:
            self.logger.info('title: {}'.format(item['title']))