from app.db import models as model
from app.db.database import SessionLocal
from app.logic.working_with_csv.load_csv import get_or_create, read_csv

db = SessionLocal()
rows = read_csv("Export.csv")
