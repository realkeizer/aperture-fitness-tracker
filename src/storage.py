import json
import csv
from pathlib import Path
from datetime import date
from daily_entry import collect_workout, get_entry

base_dir = Path(__file__).resolve().parent.parent
file_path_daily = base_dir / "data" / "daily_metrics.json"
file_path_wkt = base_dir / "data" / "workouts.json"
file_path_csv = base_dir / "data" / "yourfile.csv"

def create_json():
    file_path_daily.parent.mkdir(parents=True, exist_ok=True)

    default_structure = []

    if not file_path_daily.exists():
        with open(file_path_daily, 'w') as file:
            json.dump(default_structure, file, indent=2)

    if not file_path_wkt.exists():
        with open(file_path_wkt, 'w') as file:
            json.dump(default_structure, file, indent=2)

def auth_file(file_path):
    if file_path == file_path_daily:
        path = file_path_daily

    elif file_path == file_path_wkt:
        path = file_path_wkt

    else:
        raise ValueError("Invalid file entered for data loading. Acceptable file names are daily_metrics.json and workouts.json.")
    
    with open(path, 'r') as file:
        data = json.load(file)

    return data, path

def load_data(file_path):
    create_json()
    data, _ = auth_file(file_path)

    if not data:
        print(f"No entries found in {file_path.name}. Initialised empty JSON file.")

    else:
        print(f"Loaded {len(data)} entries from {file_path.name}")

    return data

def save_to_json(file_path):
    if file_path == file_path_daily:
        data = get_entry(file_path)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

        print(f"New entry added to {file_path.name}, total entries: {len(data)}")
    elif file_path == file_path_wkt:
        data = collect_workout()

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

#Run this function once with an altered .csv file path (seen at top of file) to migrate your CSV file to JSON format.
def migrate_csv():
    with open(file_path_csv, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        rows = list(reader)
        print(rows)

        with open(file_path_daily, 'w') as jsonfile:
            json.dump(rows, jsonfile, indent=2)

save_to_json(file_path_wkt)