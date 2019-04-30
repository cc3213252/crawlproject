# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class MastercardSpider(scrapy.Spider):
    name = 'mastercard'
    allowed_domains = ['www1.mastercard.com']
    base_url = 'https://www1.mastercard.com'
    start_urls = ['https://www1.mastercard.com/content/privileges/china/zh_cn/offers-experiences.html?country=all&cardType=all']
    lua_source = """
                    function main(splash)
                        assert(splash:go(splash.args.url))
                        for var=0,10,1 do
                            local get_dimensions = splash:jsfunc([[
                            function () {
                            var rect = document.getElementById('offerListingLoadMore').getClientRects()[0];
                            return {"x": rect.left, "y": rect.top}
                            }
                            ]])
                            splash:set_viewport_full()
                            splash:wait(0.1)
                            local dimensions = get_dimensions()
                            splash:mouse_click(dimensions.x, dimensions.y)
                            -- Wait split second to allow event to propagate.
                            splash:wait(0.5)
                        end
                        return  splash:html()
                        end
                    """
    home_splash_args = {
        'render_all': 1,
        'wait': 2,
        'lua_source': lua_source,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args=self.home_splash_args, dont_filter=True)

    def parse(self, response):
        act_urls = response.xpath('//ul[@id="offerListingResults"]/li/a/@href').getall()
        for act_url in act_urls:
            act_url = self.base_url + act_url
            self.logger.info('act_url: %s', act_url)


