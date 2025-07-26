from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class States(Base):
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    counties = relationship("Counties", back_populates="state")


class Counties(Base):
    __tablename__ = "counties"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"))
    
    state = relationship("States", back_populates="counties")
    cities = relationship("Cities", back_populates="counties")
    

class Cities(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    county_id = Column(Integer, ForeignKey("counties.id"))
    
    counties = relationship("Counties", back_populates="cities")
    markets = relationship("Markets", back_populates="cities")
    
class Markets(Base):
    __tablename__ = "markets"
    
    id = Column(Integer, primary_key=True)
    fmid = Column(Integer, unique=True)
    name = Column(String(100), nullable=False)
    website = Column(Text)
    street = Column(Text)
    city_id = Column(Integer, ForeignKey("cities.id"))
    zip = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Boolean)
    updated_at = Column(DateTime)
    
    cities = relationship("Cities", back_populates="markets")
    market_season = relationship("MarketSeason", back_populates="markets")
    
    
class MarketSeason(Base):
    __tablename__ = "market_season"
    
    id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey("market.id"))
    season_number = Column(Integer, nullable=False)
    
    markets = relationship("Markets", back_populates="market_season")
    
    
class PaymentMethod(Base):
    __trablename__ = "payment_method"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    
class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    
    
market_payment_association = Table(
    "market_payment",
    Base.metadata,
    Column("market_id", Integer, ForeignKey("markets.id"), primary_key=True),
    Column("payment_id", Integer, ForeignKey("payment_method.id"), primary_key=True)
)


market_product_association = Table(
    "market_products",
    Base.metadata,
    Column("market_id", Integer, ForeignKey("markets.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True)
)