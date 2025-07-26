from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

env = Env()
env.read_env()

db_url = env("DATABASE_URL")

engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)