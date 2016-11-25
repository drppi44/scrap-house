# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from .utils import variant_urls, location_urls
from scrap.items import HouseItem


class HouseSpider(Spider):
    name = 'house'
    allowed_domains = ['idealista.com']
    start_urls = variant_urls

    def start_requests(self):
        for variant_url in variant_urls:
            for location_url in location_urls:
                yield Request(url=variant_url+location_url, callback=self.parse)

    def parse(self, response):
        item = HouseItem()
        print response.request.url

        listings = response.xpath('//div[@class="item item_contains_branding"]/@data-adid')
        for listing in listings:
            item['id'] = listing.extract()
            yield item

        next_page_selector = 'a.icon-arrow-right-after::attr(href)'
        next_page = response.css(next_page_selector).extract_first()
        if next_page:
            yield Request(
                response.urljoin(next_page),
                callback=self.parse
            )
