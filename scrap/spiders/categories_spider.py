# -*- coding: utf-8 -*-
from scrapy.spiders import Spider


class CategorySpider(Spider):
    name = 'category'
    allowed_domains = ['idealista.com']
    start_urls = [
        'https://www.idealista.com/',
    ]

    def parse(self, response):
        selector = 'ul#location-combo li::text'
        for element in response.css(selector)[2:].extract():
            name = element.lower().replace(' ', '-')
            yield {
                'name': name,
                'url': u'https://www.idealista.com/alquiler-viviendas/%s-provincia/' % name
            }
