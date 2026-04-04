import json
from pathlib import Path
from datetime import date

base_dir = Path(__file__).resolve().parent.parent
file_path_daily = base_dir / "data" / "daily_metrics.json"
file_path_wkt = base_dir / "data" / "workouts.json"
#file_path_csv = base_dir / "data" / "YOURCSVFILEHERE.csv" -> Used for migrate_csv(). Read more above the function definition (line 34)

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

def add_entry(file_path):
    data, path = auth_file(file_path)

    datapnts_daily = {
        "Date":"",
        "Calories":0,
        "Protein":0,
        "Sleep":0,
        "Bodyweight":0
        }

    if path == file_path_daily:
        for key in datapnts_daily:
            value = input(f"Enter {key}:\n")

            if key == "Date":
                if value.strip() == "":
                    datapnts_daily["Date"] = str(date.today())
                else:
                    datapnts_daily["Date"] = value

            else:
                try:
                    datapnts_daily[key] = float(value)

                except ValueError:
                    print(f"Invalid input for {key}, setting to 0.")
                    datapnts_daily[key] = 0

        data.append(datapnts_daily)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

        print(f"New entry added to {file_path.name}, total entries: {len(data)}")
    
    elif path == file_path_wkt:
        #add_workout()
        return

# Run this function once with an altered .csv file path (seen at top of file) to migrate your CSV file to JSON format.
# def migrate_csv():
#     with open(file_path_csv, 'r') as file:
#         reader = csv.DictReader(file, delimiter=',')
#         rows = list(reader)
#         print(rows)

#         with open(file_path_daily, 'w') as jsonfile:
#             json.dump(rows, jsonfile)
# migrate_csv()