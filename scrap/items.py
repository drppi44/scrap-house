# -*- coding: utf-8 -*-
import scrapy


class HouseItem(scrapy.Item):
    id = scrapy.Field()
    # update_date = scrapy.Field()
    #
    # """ - Operation(String)
    #         + Sale - - title contains "en venta"
    #         + Rent - - title contains "Alquiler"
    #         + Share - - title contains "Alquiler de habitación"
    # """
    # operation = scrapy.Field()
    # """
    #     - Residential Sub-Type (String)
    #       + Apartment -- title contains "Piso"
    #       + Duplex -- title contains "Dúplex"
    #       + House -- title contains "Chalet" or "Casa"
    # """
    # residential_sub_type = scrapy.Field()
    # """
    #     - Commercial Sub-Type (String)
    #       + Office -- title starts with "Oficina"
    #       + Retail -- title starts with "Local"
    #       + Warehouse -- title starts with "Nave"
    # """
    # commercial_sub_type = scrapy.Field()
    # price = scrapy.Field()
    # surface = scrapy.Field()
    # """
    # - # of bedrooms (int)
    #   + # of bedrooms -- "X hab." (where X is the amount of Bedrooms)
    #   + Studio case -- title contains "Estudio"
    # """
    # bedrooms = scrapy.Field()
    # security_deposit = scrapy.Field()
    # new_construction = scrapy.Field()
    #
    # # For SHARE
    # amount_of_residents = scrapy.Field()
    # gender = scrapy.Field()
    # accept_smoke = scrapy.Field()


class CategoryItem(scrapy.Item):
    field_1 = scrapy.Field()
    field_2 = scrapy.Field()
    field_3 = scrapy.Field()
