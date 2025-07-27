import csv
from pathlib import Path

def read_csv(file_name: str):
    root_dir = Path(__file__).parent.parent.parent.parent
    csv_path = root_dir / file_name
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)