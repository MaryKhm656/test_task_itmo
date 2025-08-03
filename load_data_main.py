from app.db.database import SessionLocal
from app.logic.working_with_csv.load_data import load_data_into_db

def main():
    db = SessionLocal()
    try:
        load_data_into_db(db, "Export.csv")
        print("Загрузка данных успешно завершена!")
    except Exception as e:
        raise e
    finally:
        db.close()
        
        
if __name__ == "__main__":
    main()