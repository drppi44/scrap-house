# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from .utils import get_id_from_link, variant_urls, location_urls


class HouseSpider(Spider):
    name = 'house'
    allowed_domains = ['idealista.com']
    start_urls = variant_urls

    def parse(self, response):
        print response.request.url
        print '_'*50
        # selector = 'a.item-link::attr(href)'
        # for element in response.css(selector).extract():
        #     yield {
        #         'id': get_id_from_link(element),
        #     }
        #
        # next_page_selector = 'a.icon-arrow-right-after::attr(href)'
        # next_page = response.css(next_page_selector).extract_first()
        # if next_page:
        #     yield Request(
        #         response.urljoin(next_page),
        #         callback=self.parse
        #     )
