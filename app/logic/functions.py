from app.db.models import User
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