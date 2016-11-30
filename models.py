from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

import scrap.settings as settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_deals_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Idealista(DeclarativeBase):
    __tablename__ = 'idealista'

    id = Column(Integer, primary_key=True)
    operation = Column(String(50), nullable=True)
    residential_sub_type = Column(String(50), nullable=True)
    commercial_sub_type = Column(String(50), nullable=True)
    update_date = Column(Date, nullable=True)
    price = Column(Integer, nullable=True)
    surface = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    security_deposit = Column(String(50), nullable=True)
    new_construction = Column(Boolean, nullable=True)
    amount_of_residents = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    accept_smoke = Column(Boolean, nullable=True)
    average_age = Column(String(50), nullable=True)
    accept_occupation = Column(String(50), nullable=True)
    no_pets = Column(Boolean, nullable=True)
    has_oven = Column(Boolean, nullable=True)
    has_washing_machine = Column(Boolean, nullable=True)
    furnished = Column(Boolean, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True)
    has_cave = Column(Boolean, nullable=True)
    orientation = Column(String(50), nullable=True)
    has_terrace = Column(Boolean, nullable=True)
    parking = Column(Boolean, nullable=True)
    street_front = Column(String(50), nullable=True)
    street_corner = Column(Boolean, nullable=True)
    last_commercial_activity = Column(String(50), nullable=True)
    facade_size = Column(Integer, nullable=True)
    has_storage = Column(Boolean, nullable=True)
    has_shutter = Column(Boolean, nullable=True)
    floor = Column(String(50), nullable=True)
    has_elevator = Column(Boolean, nullable=True)
    view = Column(String(50), nullable=True)
    has_pool = Column(Boolean, nullable=True)
    has_air_condition = Column(Boolean, nullable=True)
    has_internet = Column(Boolean, nullable=True)
    location = Column(String(500), nullable=True)
    precise = Column(Boolean, nullable=True)
    agency_type = Column(String(50), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    external_link = Column(String(500), nullable=True)
    images = Column(Text, nullable=True)

