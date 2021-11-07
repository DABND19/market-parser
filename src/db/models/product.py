from datetime import datetime
import enum

from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Enum, Float, String, Text, BigInteger, DateTime

from db.models.base import Base


class Market(enum.Enum):
    WILDBERRIES = 'WILDBERRIES'


class Product(Base):
    __tablename__ = 'products'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    created_at_dt = Column(DateTime, nullable=False, default=datetime.now)
    updated_at_dt = Column(DateTime, nullable=False, default=datetime.now)

    name = Column(Text, nullable=False)
    price = Column(Float)
    market = Column(Enum(Market, name='market_enum'), nullable=False)
    original_url = Column(String(2500), nullable=False)
    competitor_id = Column(BigInteger, ForeignKey('products.id'))
