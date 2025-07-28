from app.db.database import init_db
from app.db.models import (States, Counties, Cities, Markets, MarketSeason, PaymentMethod,
                           Products, Review, User, market_product_association, market_payment_association,
                           user_review_association)

if __name__ == "__main__":
    init_db()