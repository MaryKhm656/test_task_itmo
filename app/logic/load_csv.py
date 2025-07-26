import csv
from pathlib import Path

def read_csv(sub_dir: str, file_name: str):
    path_to_csv = Path.cwd() / sub_dir / file_name

    with open(path_to_csv, 'r', encoding='utf-8') as f:
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