# -*- coding: utf-8 -*-
import locale
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from scrapy import Request
from scrapy.spiders import Spider
from scrap.items import HouseItem


from models import Idealista, db_connect, create_deals_table


class IdealistaSpider(Spider):
    name = 'idealista'
    allowed_domains = ['idealista.com']

    BASE_URL = "https://www.idealista.com/inmueble/{id}/"

    OPERATION = {
        u'en venta': 'Sale',
        u'alquiler': 'Rent',
        u'alquiler de habitación': 'Share'
    }

    RESIDENTIAL_SUB_TYPE = {
        u"piso": 'Apartment',
        u"dúplex": 'Duplex',
        u"chalet": 'House',
        u"casa": 'House'
    }

    COMMERCIAL_SUB_TYPE = {
        u"oficina": 'Office',
        u"local": 'Retail',
        u"nave": 'Warehouse'
    }

    FLOOR = {
        u'planta': 'Floor',
        u'Bajo': 'Ground floor',
        u'ático': 'Penthouse'
    }

    def __init__(self, *args, **kwargs):
        engine = db_connect()
        create_deals_table(engine)
        session = sessionmaker(bind=engine)()
        self.listings = session.query(Idealista).all()
        session.close()
        locale.setlocale(locale.LC_TIME, "es_ES")
        super(IdealistaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for listing in self.listings:
            yield Request(url=self.BASE_URL.format(id=listing.id), meta={'listing': listing})
        # yield Request(url=self.BASE_URL.format(id=31653895))

    def parse(self, response):
        item = HouseItem()
        current_listing = response.meta.get('listing', None)

        date_of_last_update = response.xpath(
            '//section[@id="stats"]/p/text()'
        ).re('Anuncio actualizado el (\d+) de (\w+)')

        today = datetime.now()
        if date_of_last_update:
            date_of_last_update = " ".join(date_of_last_update) + " " + str(today.year)

            date_of_last_update = datetime.strptime(date_of_last_update, "%d %B %Y")
            # if current_listing.update_date != None and date_of_last_update == current_listing.update_date:
            #     return
            item['update_date'] = date_of_last_update

        title = response.xpath('//section[@class="main-info"]/h1/span/text()')[0].extract().lower()
        for key, operation in self.OPERATION.items():
            if key in title:
                item['operation'] = operation

        for key, residential in self.RESIDENTIAL_SUB_TYPE.items():
            if key in title:
                item['residential_sub_type'] = residential

        for key, commercial in self.COMMERCIAL_SUB_TYPE.items():
            if key in title:
                item['commercial_sub_type'] = commercial

        price = response.xpath('//div[@class="info-data"]/span[1]/span/text()').extract()
        item['price'] = int(price[0].replace('.', '')) if price else 0

        surface = response.xpath('//div[@class="info-data"]/span[2]/span/text()').extract()
        item['surface'] = int(surface[0]) if surface else 0
        if 'commercial_sub_type' not in item.keys():
            if u'Estudio' in title:
                bedrooms = 0
            else:
                bedrooms = response.xpath('//div[@class="info-data"]/span[3]/span/text()').extract()
                bedrooms = int(bedrooms[0]) if bedrooms else 0
            item['bedrooms'] = bedrooms

        security_deposit = response.xpath('//span[@class="txt-deposit"]/span/text()').re("Fianza de (.*)")
        item['security_deposit'] = security_deposit[0] if security_deposit else ''

        new_construction = response.xpath('//span[@class="icon-new-develop"]/span/text()').re('Obra nueva')
        item['new_construction'] = True if len(new_construction) > 0 else False

        details = response.xpath('//section[@id="details"]/div/ul/li/text()')

        if item['operation'] == 'Share':
            residents = response.xpath('//div[@class="info-data"]/span[3]')

            amount = residents.xpath('./span[2]').re('\d+')
            item['amount_of_residents'] = int(amount[0]) if amount else 0

            genders = residents.xpath('./span[1]/@class').re("icon-sex-circle (\w+)")
            item['gender'] = genders[0] if genders else ''

            bedrooms = response.xpath('//div[@class="info-data"]/span[2]/span/text()').extract()
            bedrooms = int(bedrooms[0]) if bedrooms else 0
            item['bedrooms'] = bedrooms

            surface = details.re('(\d+) m\xb2')
            item['surface'] = surface[0] if surface else 0

            average_age = details.re(u'entre (\d+) y (\d+) años')
            item['average_age'] = ' - '.join(average_age) if average_age else ''

            accept_smoke = response.xpath('//span[@class="icon-no-smoking"]')
            item['accept_smoke'] = False if len(accept_smoke) > 0 else True

            no_pets = details.re(u'No se admiten mascotas')
            item['no_pets'] = True if no_pets else False

            accept_occupation = " ".join(details.extract())
            if "Estudiante" in accept_occupation:
                item['accept_occupation'] = "Estudiante"
            elif "Con trabajo" in accept_occupation:
                item['accept_occupation'] = "Con trabajo"

        description = response.xpath('//div[@class="commentsContainer"]/div/text()')[0].extract()

        item['has_oven'] = True if "horno" in description else False
        item['has_washing_machine'] = True if "lavadora" in description else False

        item['furnished'] = True if u'Totalmente amueblado y equipado' in ' '.join(details.extract()) else False

        if 'commercial_sub_type' in item.keys():
            bathrooms = details.re(u'(\d+) aseos o baños')
            item['bathrooms'] = int(bathrooms[0]) if bathrooms else 0
        else:
            bathrooms = details.re(u'(\d+) wc')
            item['bathrooms'] = int(bathrooms[0]) if bathrooms else 0

        if item['new_construction']:
            item['status'] = 'New / Recently renovated'
        else:
            item['status'] = 'Good Conditions' if details.re('Segunda mano/buen estado') else 'New / Recently renovated'

        item['has_cave'] = True if details.re('Trastero') else False
        orientation = response.xpath('//section[@id="details"]/div/ul/li/text()[contains(., "Orientaci")]')
        item['orientation'] = orientation[0].extract() if orientation else ''

        has_terrace = response.xpath('//section[@id="details"]/div/ul/li/text()[contains(., "Terraza")]')
        item['has_terrace'] = True if has_terrace else False

        parking = response.xpath('//section[@id="details"]/div/ul/li/text()[contains(., "Plaza de garaje incluida")]')
        item['parking'] = True if parking else False

        if 'commercial_sub_type' in item.keys() and item['commercial_sub_type'] == 'Retail':
            street_front = response.xpath(
                '//section[@id="details"]/div/ul/li/text()[contains(., "Situado a pie de calle")]'
            )
            item['street_front'] = street_front[0].extract() if street_front else ''

            street_corner = response.xpath(
                '//section[@id="details"]/div/ul/li/text()[contains(., "Hace esquina")]'
            )
            item['street_corner'] = True if street_corner else False

            last_commercial_activity = response.xpath(
                '//section[@id="details"]/div/ul/li/text()[contains(., "ltima actividad")]'
            )
            item['last_commercial_activity'] = last_commercial_activity[0].extract() if last_commercial_activity else ''

            facade_size = details.re("Fachada de (\d+)")
            item['facade_size'] = int(facade_size[0]) if facade_size else 0

            has_storage = response.xpath(
                '//section[@id="details"]/div/ul/li/text()[contains(., "archivo")]'
            )
            item['has_storage'] = True if has_storage else False

            has_shutter = response.xpath(
                '//section[@id="details"]/div/ul/li/text()[contains(., "Puerta de seguridad")]'
            )
            item['has_shutter'] = True if has_shutter else False

        for key, floor in self.FLOOR.items():
            planta = response.xpath(
                '//section[@id="details"]/div/ul/li/text()[contains(., translate("'+key+'", "p", "P"))]'
            ).extract()
            if planta and 'planta' in planta[0].lower():
                item['floor'] = planta[0]
            elif planta:
                item['floor'] = floor

        if u'ático' in title:
            item['floor'] = self.FLOOR[u'ático']

        has_elevator = response.xpath('//section[@id="details"]/div/ul/li/text()[contains(.,"Sin ascensor")]').extract()
        item['has_elevator'] = False if has_elevator else True

        view = response.xpath('//section[@id="details"]/div/ul/li/text()[contains(.,"exterior")]').extract()
        item['view'] = 'Exterior' if view else 'Interior'

        has_pool = response.xpath('//section[@id="details"]/div/ul/li/text()[contains(.,"Piscina")]').extract()
        item['has_pool'] = True if has_pool else False

        has_air_condition = response.xpath(
            '//section[@id="details"]/div/ul/li/text()[contains(.,"Aire acondicionado")]'
        ).extract()
        item['has_air_condition'] = True if has_air_condition else False

        has_internet = response.xpath(
            '//section[@id="details"]/div/ul/li/text()[contains(.,"internet")]'
        ).extract()
        item['has_internet'] = True if has_internet else False

        location = " ".join(response.xpath('//div[@id="addressPromo"]/ul/li/text()').extract())
        item['location'] = location.strip()

        precise = response.xpath('//a[contains(@class, "icon-location")]')
        item['precise'] = True if precise else False

        agency_type = response.xpath('//div[contains(@class, "advertiser-data")]/p/text()[contains(., "Profesional")]')
        item['agency_type'] = 'Professional' if agency_type else 'Particular'

        images = response.xpath('//img/@data-service').extract()
        item['images'] = []
        for img in images:
            item['images'].append(img.split(',')[0])

        contact_phone = response.xpath('//div[@class="contact-phones"]/div/p/text()').extract()
        item['contact_phone'] = contact_phone[0].strip() if contact_phone else ''

        external_link = response.xpath('//a[@id="linkAdicional"]/@href').extract()
        item['external_link'] = external_link[0] if external_link else ''

        yield item

