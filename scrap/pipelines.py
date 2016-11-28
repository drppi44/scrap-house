# -*- coding: utf-8 -*-
from scrapy import signals
from models import Idealista


class ScrapPipeline(object):
    session = None

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        pass

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.session = spider.session

    def spider_closed(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        try:
            listing = Idealista(id=item.get('id', None))
            existing_query_listing = self.session.query(Idealista).filter(Idealista.id == listing.id).first()
            if existing_query_listing:
               listing = existing_query_listing
            else:
                self.session.add(listing)
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()

        return item
