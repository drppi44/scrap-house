# -*- coding: utf-8 -*-
import locale
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from elixir import setup_all, create_all

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.utils.response import open_in_browser
from scrap.items import HouseItem


from models import Idealista


class IdealistaSpider(Spider):
    name = 'idealista'
    allowed_domains = ['idealista.com']

    BASE_URL = "https://www.idealista.com/inmueble/{id}/"

    OPERATION = {
        u'en venta': 'Sale',
        u'Alquiler': 'Rent',
        u'Alquiler de habitación': 'Share'
    }

    RESIDENTIAL_SUB_TYPE = {
        u"Piso": 'Apartment',
        u"Dúplex": 'Duplex',
        u"Chalet": 'House',
        u"Casa": 'House'
    }

    COMMERCIAL_SUB_TYPE = {
        u"Oficina": 'Office',
        u"Local": 'Retail',
        u"Nave": 'Warehouse'
    }

    def __init__(self, *args, **kwargs):
        setup_all()
        create_all()
        self.session = sessionmaker()()
        self.listings = self.session.query(Idealista).all()
        locale.setlocale(locale.LC_TIME, "es_ES")
        super(IdealistaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        # for listing in self.listings[0:2]:
        #     yield Request(url=self.BASE_URL.format(id=listing.id), meta={'listing': listing})
        yield Request(url=self.BASE_URL.format(id=31653895))

    def parse(self, response):
        item = HouseItem()
        # open_in_browser(response)
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

        title = response.xpath('//section[@class="main-info"]/h1/span/text()')[0].extract()
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

            item['street_front'] = street_front






        yield item

