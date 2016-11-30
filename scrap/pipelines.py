# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from scrapy import signals
from models import Idealista, db_connect, create_deals_table


class ScrapPipeline(object):
    session = None

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    # @classmethod
    # def from_crawler(cls, crawler):
    #     pipeline = cls()
    #     crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    #     crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    #     return pipeline
    #
    # def spider_opened(self, spider):
    #     self.session = sessionmaker()()
    #
    # def spider_closed(self, spider):
    #     self.session.close()

    def process_item(self, item, spider):
        session = self.Session()
        try:
            listing = Idealista(id=item.get('id', None))
            existing_listing = session.query(Idealista).filter(Idealista.id == listing.id).first()

            listing.operation = item.get('operation', existing_listing.operation if existing_listing else None)
            listing.residential_sub_type = item.get('residential_sub_type',
                                                    existing_listing.residential_sub_type if existing_listing else None)
            listing.commercial_sub_type = item.get('commercial_sub_type',
                                                   existing_listing.commercial_sub_type if existing_listing else None)
            listing.update_date = item.get('update_date', existing_listing.update_date if existing_listing else None)
            listing.price = item.get('price', existing_listing.price if existing_listing else None)
            listing.surface = item.get('surface', existing_listing.surface if existing_listing else None)
            listing.bedrooms = item.get('bedrooms', existing_listing.bedrooms if existing_listing else None)
            listing.security_deposit = item.get('security_deposit',
                                                existing_listing.security_deposit if existing_listing else None)
            listing.new_construction = item.get('new_construction',
                                                existing_listing.new_construction if existing_listing else None)
            listing.amount_of_residents = item.get('amount_of_residents',
                                                   existing_listing.amount_of_residents if existing_listing else None)
            listing.gender = item.get('gender', existing_listing.gender if existing_listing else None)
            listing.accept_smoke = item.get('accept_smoke', existing_listing.accept_smoke if existing_listing else None)
            listing.average_age = item.get('average_age', existing_listing.average_age if existing_listing else None)
            listing.accept_occupation = item.get('accept_occupation',
                                                 existing_listing.accept_occupation if existing_listing else None)
            listing.no_pets = item.get('no_pets', existing_listing.no_pets if existing_listing else None)
            listing.has_oven = item.get('has_oven', existing_listing.has_oven if existing_listing else None)
            listing.has_washing_machine = item.get('has_washing_machine',
                                                   existing_listing.has_washing_machine if existing_listing else None)
            listing.furnished = item.get('furnished', existing_listing.furnished if existing_listing else None)
            listing.bathrooms = item.get('bathrooms', existing_listing.bathrooms if existing_listing else None)
            listing.status = item.get('status', existing_listing.status if existing_listing else None)
            listing.has_cave = item.get('has_cave', existing_listing.has_cave if existing_listing else None)
            listing.orientation = item.get('orientation', existing_listing.orientation if existing_listing else None)
            listing.has_terrace = item.get('has_terrace', existing_listing.has_terrace if existing_listing else None)
            listing.parking = item.get('parking', existing_listing.parking if existing_listing else None)
            listing.street_front = item.get('street_front', existing_listing.street_front if existing_listing else None)
            listing.street_corner = item.get('street_corner',
                                             existing_listing.street_corner if existing_listing else None)
            listing.last_commercial_activity = item.get(
                'last_commercial_activity',
                existing_listing.last_commercial_activity if existing_listing else None)
            listing.facade_size = item.get('facade_size', existing_listing.facade_size if existing_listing else None)
            listing.has_storage = item.get('has_storage', existing_listing.has_storage if existing_listing else None)
            listing.has_shutter = item.get('has_shutter', existing_listing.has_shutter if existing_listing else None)
            listing.floor = item.get('floor', existing_listing.floor if existing_listing else None)
            listing.has_elevator = item.get('has_elevator', existing_listing.has_elevator if existing_listing else None)
            listing.view = item.get('view', existing_listing.view if existing_listing else None)
            listing.has_pool = item.get('has_pool', existing_listing.has_pool if existing_listing else None)
            listing.has_air_condition = item.get('has_air_condition',
                                                 existing_listing.has_air_condition if existing_listing else None)
            listing.has_internet = item.get('has_internet', existing_listing.has_internet if existing_listing else None)
            listing.location = item.get('location', existing_listing.location if existing_listing else None)
            listing.precise = item.get('precise', existing_listing.precise if existing_listing else None)
            listing.agency_type = item.get('agency_type', existing_listing.agency_type if existing_listing else None)
            listing.contact_phone = item.get('contact_phone',
                                             existing_listing.contact_phone if existing_listing else None)
            listing.external_link = item.get('external_link',
                                             existing_listing.external_link if existing_listing else None)
            images = item.get('images', )
            listing.images = ';'.join(images) if images else (existing_listing.images if existing_listing else "")
            print(listing)
            if not existing_listing:
                print('I am here')
                session.add(listing)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
