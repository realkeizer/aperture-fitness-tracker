import json
import csv
from pathlib import Path
from datetime import date

base_dir = Path(__file__).resolve().parent.parent
file_path_daily = base_dir / "data" / "daily_metrics.json"
file_path_wkt = base_dir / "data" / "workouts.json"
file_path_csv = base_dir / "data" / "yourfile.csv"

# Class object for collecting standard daily metrics
class MacroEntry:
    def __init__(self, Date, Calories, Protein, Sleep, Bodyweight):
        self.Date = str(Date)
        self.Calories = float(Calories)
        self.Protein = float(Protein)
        self.Sleep = float(Sleep)
        self.Bodyweight = float(Bodyweight)
    def to_dict(self):
        return self.__dict__

# Separate classes for different data layers (date, exercises, sets, reps, etc)
class SetEntry():
    def __init__(self, weight: float, reps: int):
        self.weight = weight
        self.reps = reps
    def volume(self):
        return self.weight * self.reps
    def to_dict(self):
        return self.__dict__

class ExerciseEntry():
    def __init__(self, name: str):
        self.name = name
        self.sets: list[SetEntry] = []
    
    def add_set(self, set_entry: SetEntry):
        self.sets.append(set_entry)
    
    def total_volume(self):
        return sum(s.volume() for s in self.sets)
    
    def to_dict(self):
        return {
            "name": self.name,
            "sets": [s.to_dict() for s in self.sets]
        }
    
class WorkoutSession:
    def __init__(self, date: str, session_type: str):
        self.date = date
        self.session_type = session_type
        self.exercises: list[ExerciseEntry] = []

    def add_exercise(self, exercise: ExerciseEntry):
        self.exercises.append(exercise)
    def total_volume(self):
        return sum(ex.total_volume for ex in self.exercises)
    def to_dict(self):
        return {
            "date": self.date,
            "session_type": self.session_type,
            "exercises": [ex.to_dict() for ex in self.exercises]
        }

def collect_workout():
    date = input("Date: ")
    session_type = input("Session type (i.e 'Strength'): ")

    workout = WorkoutSession(date, session_type)

    num_exercises = int(input("How many exercises did you do? "))

    for _ in range(num_exercises):
        exercise_name = input("Exercise name: ")
        exercise = ExerciseEntry(exercise_name)

        num_sets = int(input("How many sets did you do?"))

        for set_num in range(1, num_sets + 1):
            weight = float(input(f"Set {set_num} weight: "))
            reps = int(input(f"Set {set_num} reps: "))

            exercise.add_set(SetEntry(weight, reps))

        workout.add_exercise(exercise)
    return workout.to_dict()

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

def get_entry(file_path):
    data, path = auth_file(file_path)
    metrics = {
        "Date": str,
        "Calories": int,
        "Protein": int,
        "Sleep": float,
        "Bodyweight": float
    }
    if path == file_path_daily:
        for key in metrics:
            value = input(f"Enter {key}:\n")

            if key == "Date":
                if value.strip() == "":
                    metrics["Date"] = str(date.today())
                else:
                    metrics["Date"] = date.strptime(value, "%Y-%m-%d")

            else:
                try:
                    metrics[key] = float(value)

                except ValueError:
                    print(f"Invalid input for {key}, setting to 0.")
                    metrics[key] = 0

        entry = MacroEntry(**metrics)
        data.append(entry.to_dict())
        return data
    
    elif path == file_path_wkt:
        #add_workout()
        return #data

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