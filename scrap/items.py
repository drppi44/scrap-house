# -*- coding: utf-8 -*-
import scrapy


class HouseItem(scrapy.Item):
    id = scrapy.Field()


class CategoryItem(scrapy.Item):
    field_1 = scrapy.Field()
    field_2 = scrapy.Field()
    field_3 = scrapy.Field()
