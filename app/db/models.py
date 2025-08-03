from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


market_payment_association = Table(
    "market_payment",
    Base.metadata,
    Column("market_id", Integer, ForeignKey("markets.id"), primary_key=True),
    Column("payment_id", Integer, ForeignKey("payment_methods.id"), primary_key=True)
)


market_product_association = Table(
    "market_products",
    Base.metadata,
    Column("market_id", Integer, ForeignKey("markets.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True)
)



class States(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    county = relationship("Counties", back_populates="state")

    def __str__(self):
        return f"State:\nid={self.id}\nname={self.name}"


class Counties(Base):
    __tablename__ = "counties"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"))

    state = relationship("States", back_populates="county")
    cities = relationship("Cities", back_populates="county")

    def __str__(self):
        return f"County:\nid={self.id}\nname={self.name}\nstate id={self.state_id}"


class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    county_id = Column(Integer, ForeignKey("counties.id"))

    county = relationship("Counties", back_populates="cities")
    markets = relationship("Markets", back_populates="cities")

    def __str__(self):
        return f"City:\nid{self.id}\nname={self.name}\ncounty id={self.county_id}"

class Markets(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True)
    fmid = Column(Integer, unique=True)
    name = Column(String(100), nullable=False)
    rating = Column(Float)
    website = Column(Text)
    street = Column(Text)
    city_id = Column(Integer, ForeignKey("cities.id"))
    zip = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    has_location = Column(Boolean)
    updated_at = Column(DateTime)

    reviews = relationship("Review", back_populates="markets")
    cities = relationship("Cities", back_populates="markets")
    market_seasons = relationship("MarketSeason", back_populates="markets")
    payment_methods = relationship("PaymentMethod", secondary=market_payment_association, back_populates="markets")
    products = relationship("Products", secondary=market_product_association, back_populates="markets")

    def __str__(self):
        return (f"Market:"
                f"\nid={self.id}"
                f"\nname={self.name}"
                f"\ncity id={self.city_id}")


class MarketSeason(Base):
    __tablename__ = "market_season"

    id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey("markets.id"))
    season_number = Column(Integer, nullable=False)
    date_range = Column(Text)
    time_schedule = Column(Text)

    markets = relationship("Markets", back_populates="market_seasons")

    def __str__(self):
        return (f"Season:"
                f"\nid={self.id}"
                f"\nmarket_id={self.market_id}"
                f"\nseason number={self.season_number}")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    markets = relationship("Markets", secondary=market_payment_association, back_populates="payment_methods")

    def __str__(self):
        return (f"PayMethod:"
                f"\nid={self.id}"
                f"\nname={self.name}")

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    markets = relationship("Markets", secondary=market_product_association, back_populates="products")

    def __str__(self):
        return (f"Product:"
                f"\nid={self.id}"
                f"\nname={self.name}")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey("markets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    review_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="reviews")
    markets = relationship("Markets", back_populates="reviews")

    def __str__(self):
        return (f"Review:"
                f"\nid={self.id}"
                f"\nmarket_id={self.market_id}"
                f"\nuser_id={self.user_id}"
                f"\nrating={self.rating}"
                f"\nreview={self.review_text}")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), default=None)
    created_at = Column(DateTime, default=datetime.now)

    reviews = relationship("Review", back_populates="user")

    def __str__(self):
        return (f"User:"
                f"\nid={self.id}"
                f"\nName={self.first_name} {self.last_name}")