# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from models import Idealista, db_connect, create_deals_table
from functools import partial
from .spiders.utils import field_names


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
        self.item = None
        self.listing = None
        self.existing_listing = None

    @staticmethod
    def set_listing_property(listing, item, existing_listing, prop_name):
        item_value = item.get(prop_name, None)
        existing_listing_value = getattr(existing_listing, prop_name, None)
        setattr(listing, prop_name, item_value or existing_listing_value)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            listing = Idealista(id=item.get('id', None))
            existing_listing = session.query(Idealista).filter(
                Idealista.id == listing.id
            ).first()
            for field_name in field_names:
                self.set_listing_property(
                    listing,
                    item,
                    existing_listing,
                    field_name
                )

            images = ';'.join(item.get('images', [])) or \
                     getattr(existing_listing, 'images', None)
            listing.images = images
            if not existing_listing:
                session.add(listing)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
