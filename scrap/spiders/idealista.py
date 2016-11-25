# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from .utils import variant_urls, location_urls
from scrap.items import HouseItem


class IdealistaSpider(Spider):
    name = 'idealista'
    allowed_domains = ['idealista.com']

    BASE_URL = "https://www.idealista.com/inmueble/{id}/"

    def parse(self, response):
        item = HouseItem()
        print response.request.url
