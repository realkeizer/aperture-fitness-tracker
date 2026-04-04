import json
import pandas
from storage import file_path_daily, file_path_wkt, auth_file

def print_entries(file_path):
    _, path = auth_file(file_path) 
    
    with open(path, 'r') as file:
        contents = file.read()
        jsonconvert = json.loads(contents)
        jsonformat = json.dumps(jsonconvert, indent=2)
        print(jsonformat)