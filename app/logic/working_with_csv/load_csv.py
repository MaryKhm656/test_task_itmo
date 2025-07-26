import csv
from pathlib import Path

def read_csv(file_name: str):
    csv_path = Path(file_name)
    
    with csv_path.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_or_create(db, model, filter_kwargs, create_kwargs=None):
    instance = db.query(model).filter_by(**filter_kwargs).first()
    if not instance:
        data = filter_kwargs.copy()
        if create_kwargs:
            data.update(create_kwargs)
        instance = model(**data)
        db.add(instance)
        db.flush()
    return instance