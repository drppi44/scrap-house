# -*- coding: utf-8 -*-
import scrapy


class HouseItem(scrapy.Item):
    id = scrapy.Field()
    update_date = scrapy.Field()

    # """ - Operation(String)
    #         + Sale - - title contains "en venta"
    #         + Rent - - title contains "Alquiler"
    #         + Share - - title contains "Alquiler de habitación"
    # """
    operation = scrapy.Field()

    # """
    #     - Residential Sub-Type (String)
    #       + Apartment -- title contains "Piso"
    #       + Duplex -- title contains "Dúplex"
    #       + House -- title contains "Chalet" or "Casa"
    # """
    residential_sub_type = scrapy.Field()

    # """
    #     - Commercial Sub-Type (String)
    #       + Office -- title starts with "Oficina"
    #       + Retail -- title starts with "Local"
    #       + Warehouse -- title starts with "Nave"
    # """
    commercial_sub_type = scrapy.Field()

    price = scrapy.Field()
    surface = scrapy.Field()

    # """
    # - # of bedrooms (int)
    #   + # of bedrooms -- "X hab." (where X is the amount of Bedrooms)
    #   + Studio case -- title contains "Estudio"
    # """
    bedrooms = scrapy.Field()

    security_deposit = scrapy.Field()
    new_construction = scrapy.Field()

    # --- For SHARE ---
    amount_of_residents = scrapy.Field()

    # - Accepted Gender / s(String) - - "Chica" or "Chico" or "Chico o chica, da igual"
    gender = scrapy.Field()
    accept_smoke = scrapy.Field()

    # - Residents Average Age -- "Ahora son .. entre X y Y años"  (X and Y the range of age)
    average_age = scrapy.Field()

    # - Accepted Occupation/s (String) -- "Estudiante" or "Con trabajo"
    accept_occupation = scrapy.Field()

    no_pets = scrapy.Field()
    # -------

    # - Has Oven(boolean) - - if found term "horno"
    has_oven = scrapy.Field()

    # Has Washing machine (boolean) -- if found term "lavadora"
    has_washing_machine = scrapy.Field()

    # - Furnished(String)
    #   + Is furnished - - "Totalmente amueblado y equipado"

    furnished = scrapy.Field()
    #  - # of bathrooms (int)
    #   -- for Residential "X wc"
    #   -- for Commercial "X aseos o baños"
    bathrooms = scrapy.Field()

    #  - Status (String)
    #   + New / Recently renovated
    #   + Good Conditions -- "Segunda mano/buen estado"
    status = scrapy.Field()

    # - Has Cave/Storage (boolean) -- "Trastero"
    has_cave = scrapy.Field()

    # - Orientation (String) -- example "Orientación norte, oeste" or "Orientación este"
    orientation = scrapy.Field()

    # Has Terrace (boolean) -- if it has "Terraza" in Características básicas
    has_terrace = scrapy.Field()

    # Parking (boolean) -- "Plaza de garaje incluida"
    parking = scrapy.Field()

    #  - Street front (String) -- "Situado a pie de calle"
    street_front = scrapy.Field()

    # - Street corner (boolean) -- "Hace esquina"
    street_corner = scrapy.Field()

    # - Last Commercial Activity (String) -- "Última actividad: XXXX"  (where XXXX is the last activity)
    last_commercial_activity = scrapy.Field()


class CategoryItem(scrapy.Item):
    field_1 = scrapy.Field()
    field_2 = scrapy.Field()
    field_3 = scrapy.Field()
