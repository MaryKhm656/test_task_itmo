import math
from statistics import mean

from sqlalchemy.orm import joinedload

from app.db.models import User, Markets, Cities, Counties, States, Review
from app.db.database import SessionLocal

def create_user(db: SessionLocal, username: str, first_name: str, last_name: str = None):

        if not first_name.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        try:
            existing_user = db.query(User).filter(User.username==username).first()
            if existing_user:
                raise ValueError("Пользователь с таким username уже существует")
            new_user = User(username=username, first_name=first_name, last_name=last_name)
            db.add(new_user)
            db.commit()
            return new_user
        except Exception as e:
            raise e
        
        
def get_user(db: SessionLocal, username: str):
    try:
        user = db.query(User).filter(User.username==username).first()
        if not user:
            raise ValueError("Пользователь с таким username не найден")
        return user
    except Exception as e:
        raise e


def get_all_markets(db: SessionLocal, page: int = 1, per_page: int = 5):

    try:
        query = db.query(Markets).options(joinedload(Markets.reviews)).all()
        total_pages = math.ceil(len(query) / per_page)
        markets = query[(page - 1) * per_page: page * per_page]
        return markets, total_pages
    except Exception as e:
        raise e


def get_market_by_id(db: SessionLocal, market_id: int):

    try:
        market = db.query(Markets).filter(Markets.id == market_id).first()
        if not market:
            raise ValueError("Рынок с таким ID не найден")
        return market
    except Exception as e:
        raise e

def search_markets_by_location(db: SessionLocal, city: str = None, state: str = None, zip_code: int = None):
    try:
        if state is None and city is None and zip_code is None:
            raise ValueError("Введите хотя бы одно значение")
        query = db.query(Markets).join(Cities).join(Counties).join(States)
        if city:
            query = query.filter(Cities.name.ilike(f"%{city}%"))
        if state:
            query = query.filter(States.name.ilike(f"%{state}%"))
        if zip_code:
            query = query.filter(Markets.zip == zip_code)
        return query.all()
    except Exception as e:
        raise e


def get_reviews_by_market(db: SessionLocal, market_id: int):
    return db.query(Review).filter_by(market_id=market_id).all()


def update_market_rating(db: SessionLocal, market_id: int):
    reviews = get_reviews_by_market(db, market_id)
    market = db.query(Markets).filter_by(id=market_id).first()
    if not market:
        print("Магазин с таким ID Не найден")
    if not reviews:
        return
    avg_rating = mean(reviews)
    market.rating = round(avg_rating, 1)
    db.commit()


def add_review(db: SessionLocal, market_id: int, username: str, rating: int, text: str = ""):

    try:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            raise ValueError("Пользователь с таким username не найден")

        review = Review(
            market_id=market_id,
            user_id=user.id,
            rating=rating,
            review_text=text
        )
        db.add(review)
        # db.commit()
        update_market_rating(db, market_id)
        return review
    except Exception as e:
        db.rollback()
        raise e


def delete_review(db: SessionLocal, review_id: int):
    try:
        review = db.query(Review).get(review_id)
        if not review:
            raise ValueError("Отзыв с таким ID Не найден!")
        db.delete(review)
        db.commit()
        print("Отзыв успешно удален!")
    except Exception as e:
        raise e


def delete_user(db: SessionLocal, user_id: int):
    try:
        user = db.query(User).get(user_id)
        if not user:
            raise ValueError("Пользователь с таким ID не найден!")
        db.delete(user)
        db.commit()
        print("Пользователь успешно удален!")
    except Exception as e:
        raise e