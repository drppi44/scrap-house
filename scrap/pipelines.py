# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from elixir import setup_all, create_all, session
from models import Idealista


class ScrapPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        setup_all()
        create_all()
        self.session = sessionmaker()()

    def process_item(self, item, spider):
        try:
            listing = Idealista(id=item.get('id', None))
            print listing.id
            existing_query_listing = session.query(Idealista).filter(
                Idealista.id == listing.id).first()
            print existing_query_listing
            if existing_query_listing:
               listing = existing_query_listing
            else:
                session.add(listing)
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()

        return item
