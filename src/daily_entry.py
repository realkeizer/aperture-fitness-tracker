from storage import file_path_daily, file_path_wkt, auth_file
from datetime import datetime, date
import json

class MacroEntry: # Class object for daily metrics
    def __init__(self, Date, Calories, Protein, Sleep, Bodyweight):
        self.Date = str(Date)
        self.Calories = float(Calories)
        self.Protein = float(Protein)
        self.Sleep = float(Sleep)
        self.Bodyweight = float(Bodyweight)
    def to_dict(self):
        return self.__dict__

class SetEntry(): # Class Object for Collecting Reps and Weight
    def __init__(self, weight: float, reps: int):
        self.weight = weight
        self.reps = reps
    def volume(self):
        return self.weight * self.reps
    def to_dict(self):
        return self.__dict__

class ExerciseEntry(): # Class Object for Collecting Exercise Names, Sets = Length of SetEntry Dictionary
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
    
class WorkoutSession: # Class Object for Collecting Workout Type and Number of Exercises Done
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

class RuckMarch: # Class Object with Ruck March Data
    def __init__(self, date, name, weight, speed, distance, duration):
        self.date = date
        self.name = name
        self.weight = weight
        self.speed = speed
        self.distance = distance
        self.duration = duration
    def to_dict(self):
        return self.__dict__

def get_entry(file_path): # Function to Collect Daily Metrics
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

def collect_rkmch(session_type): # Logic for recording Ruck Marches
    name = "Ruck March"
    date = input("Date: ")
    if session_type.lower() != "ruck march":
        raise ValueError("Wrong session type called for this function. (Needs to be a Ruck March)")
    
    weight: float = input("How much in KG were you carrying?")
    distance: float = float(input("How far in KM did you travel?"))
    duration: str = input("How long did it take?")

    time_obj = datetime.strptime(duration, "%H:%M:%S").time()
    
    hours = (
        time_obj.hour 
        + time_obj.minute / 60 
        + time_obj.second / 3600
        )
    speed: float = round(distance / hours, 2)
    session = RuckMarch(date, name, weight, speed, duration, hours)
    return session.__dict__

def collect_wtlft(session_type): # Logic for recording weightlifting sessions
    date = input("Date: ")
    if session_type in ["Strength", "strength", "Hypertrophy", "hypertrophy"]:
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
    else:
        raise ValueError("Wrong session type called for this function. (Needs to be Weightlifting)")
    return workout.to_dict()

def collect_workout(): # Conditional statements to check which type of workout it was
    session_type = input("What type of session did you do today?").strip().lower()
    if session_type in ["strength", "hypertrophy"]:
        print(f"You performed a {session_type} session.")
        trained = collect_wtlft(session_type)
    elif session_type in ["ruck march"]:
        print(f"You performed a {session_type} session.")
        trained = collect_rkmch(session_type)
    return trained

def save_to_json(file_path): # Logic for Saving Entries to Json Files
    if file_path == file_path_daily:
        data = get_entry(file_path)
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
        existing_data.append(data)
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=2)

        print(f"New entry added to {file_path.name}, total entries: {len(existing_data)}")
    elif file_path == file_path_wkt:
        data = collect_workout()
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
        existing_data.append(data)
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=2)
        print(f"New entry added to {file_path.name}, total entries: {len(existing_data)}")