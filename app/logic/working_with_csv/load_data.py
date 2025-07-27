from datetime import datetime
from app.db.models import States, Counties, Cities, Markets, MarketSeason, PaymentMethod, Products, market_product_association, market_payment_association
from app.db.database import SessionLocal
from app.logic.working_with_csv.load_csv import read_csv
from sqlalchemy.orm import Session
from app.logic.working_with_csv.constants import PAYMENT_METHODS_MAPPING, PRODUCTS_MAPPING


def insert_states(db: Session, data: list[dict]):
    states = {row['State'] for row in data if row.get('State')}
    
    for state_name in states:
        ex_state = db.query(States).filter(States.name == state_name).first()
        if not ex_state:
            db.add(States(name=state_name))
        db.commit()
        
def insert_counties(db: Session, data: list[dict]):
    state_counties = {(row['State'], row['County']) for row in data if row.get("County")}
    
    for state_name, county_name in state_counties:
        state = db.query(States).filter(States.name == state_name).first()
        if not state:
            continue
        existing_county = (
            db.query(Counties).
            filter(Counties.name == county_name, Counties.state_id == state.id)
            .first()
        )
        if not existing_county:
            db.add(Counties(name=county_name, state_id=state.id))
            
    db.commit()
        
        
def insert_cities(db: Session, data: list[dict]):
    locations = {
        (row['State'], row['County'], row['city'])
        for row in data
        if row.get('city') and row.get('County')
    }
    
    for state_name, county_name, city_name in locations:
        county = (
            db.query(Counties)
            .join(States)
            .filter(States.name == state_name, Counties.name == county_name)
            .first()
        )
        
        if not county:
            continue
            
        exist_city = (
            db.query(Cities)
            .filter(Cities.name == city_name, Cities.county_id == county.id)
            .first()
        )
        
        if not exist_city:
            db.add(Cities(name=city_name, county_id=county.id))
            
    db.commit()
    
    
def insert_payment_methods(db: Session):
    for name in PAYMENT_METHODS_MAPPING.values():
        existing = db.query(PaymentMethod).filter(PaymentMethod.name == name).first()
        if not existing:
            db.add(PaymentMethod(name=name))
    db.commit()
    
    
def insert_products(db: Session):
    for name in PRODUCTS_MAPPING.values():
        exist_name = db.query(Products).filter(Products.name == name).first()
        if not exist_name:
            db.add(Products(name=name))
    db.commit()
    
    
def insert_markets(db: Session, data: list[dict]):
    for row in data:
        city = (
            db.query(Cities)
            .join(Counties)
            .join(States)
            .filter(
                States.name == row['State'],
                Counties.name == row['County'],
                Cities.name == row['city']
            )
            .first()
        )
        if not city:
            continue
        
        ex_market = db.query(Markets).filter(Markets.fmid == row['FMID']).first()
        if ex_market:
            continue
            
        market = Markets(
            fmid=row["FMID"],
            name=row["MarketName"],
            website=row.get("Website"),
            street=row.get("street"),
            city_id=city.id,
            zip=row.get("zip"),
            latitude=float(row["y"]) if row.get("y") else None,
            longitude=float(row["x"]) if row.get("x") else None,
            location=row.get("Location") == "Y",
            updated_at=datetime.strptime(row["updateTime"], "%m/%d/%Y %I:%M:%S %p") if row.get("updateTime") else None,
        )
        db.add(market)
        db.flush()

        insert_market_seasons(db, market.id, row)
        insert_market_payments(db, market.id, row)
        insert_market_products(db, market.id, row)
        
    db.commit()
    
    
def insert_market_seasons(db: Session, market_id: int, row: dict):
    for season_num in range(1, 5):
        date_key = f"Season{season_num}Date"
        time_key = f"Season{season_num}Time"
        
        if row.get(date_key):
            season = MarketSeason(
                market_id=market_id,
                season_number=season_num,
                date_range=row[date_key],
                time_schedule=row.get(time_key)
            )
            db.add(season)
    
    
def insert_market_payments(db: Session, market_id: int, row: dict):
    for csv_col, payment_name in PAYMENT_METHODS_MAPPING.items():
        if row.get(csv_col) == "Y":
            payment = db.query(PaymentMethod).filter(PaymentMethod.name == payment_name).first()
            if payment:
                existing_link = (
                    db.query(market_payment_association)
                    .filter_by(market_id=market_id, payment_id=payment.id)
                    .first()
                )
                if not existing_link:
                    db.execute(
                        market_payment_association.insert(),
                        {"market_id": market_id, "payment_id": payment.id},
                    )


def insert_market_products(db: Session, market_id: int, row: dict):
    for csv_col, product_name in PRODUCTS_MAPPING.items():
        if row.get(csv_col) == "Y":
            product = db.query(Products).filter(Products.name == product_name).first()
            if product:
                existing_link = (
                    db.query(market_product_association)
                    .filter_by(market_id=market_id, product_id=product.id)
                    .first()
                )
                if not existing_link:
                    db.execute(
                        market_product_association.insert(),
                        {"market_id": market_id, "product_id": product.id},
                    )


def load_data_into_db(db: Session, csv_path: str):
    data = read_csv(csv_path)

    insert_states(db, data)
    insert_counties(db, data)
    insert_cities(db, data)
    insert_payment_methods(db)
    insert_products(db)

    insert_markets(db, data)