import csv
from pathlib import Path

def read_csv(file_name: str):
    root_dir = Path(__file__).parent.parent.parent.parent
    csv_path = root_dir / file_name
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
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