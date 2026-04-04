import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
file_path_daily = base_dir / "data" / "daily_metrics.json"
file_path_wkt = base_dir / "data" / "workouts.json"
#file_path_csv = base_dir / "data" / "wellness_data.csv" -> Used for migrate_csv(). Read more above the function definition (line 34)

def create_json():
    file_path_daily.parent.mkdir(parents=True, exist_ok=True)

    default_structure = []

    if not file_path_daily.exists():
        with open(file_path_daily, 'w') as file:
            json.dump(default_structure, file, index=2)
            
    if not file_path_wkt.exists():
        with open(file_path_wkt, 'w') as file:
            json.dump(default_structure, file, index=2)

def add_entry():
    datapnts = {"Date":"", "Calories":"", "Protein":"", "Sleep":"", "Bodyweight":""}
    for key in datapnts:
        datapnts[key] = input(f"Enter {key}:\n")
    with open(file_path_daily, 'w') as file:
        json.dump(datapnts, file)

def print_entries_daily():
    with open(file_path_daily, 'r') as file:
        contents = file.read()
        jsonconvert = json.loads(contents)
        jsonformat = json.dumps(jsonconvert, indent=2)
        print(jsonformat)

def print_entries_wkt():
    with open(file_path_wkt, 'r') as file:
        contents = file.read()
        jsonconvert = json.loads(contents)
        jsonformat = json.dumps(jsonconvert, indent=2)
        print(jsonformat)

def load_data(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
        return contents

# Run this function once with an altered .csv file path to migrate your CSV file to JSON format.
# def migrate_csv():
#     with open(file_path_csv, 'r') as file:
#         reader = csv.DictReader(file, delimiter=',')
#         rows = list(reader)
#         print(rows)
#         with open(file_path_daily, 'w') as jsonfile:
#             json.dump(rows, jsonfile)
