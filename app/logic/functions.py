import math

from sqlalchemy.orm import joinedload, sessionmaker

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
            db.refresh()
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
        query = db.query(Markets).optioms(joinedload(Markets.reviews)).all()
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


def add_review(db: SessionLocal, market_id: int, user_name: str, rating: int, text: str = ""):

    try:
        user = db.query(User).filter(username=user_name).first()
        if not user:
            raise ValueError("Пользователь с таким username не найден")

        review = Review(
            market_id=market_id,
            user_id=user.id,
            rating=rating,
            review_text=text
        )
        db.add(review)
        db.commit()
        db.refresh()
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