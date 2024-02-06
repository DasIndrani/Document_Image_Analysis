import os
import json, dump

Output_folder = "Output"
os.makedirs(Output_folder, exist_ok=True)


def save_object(response,reset):
    filepath = os.listdir(Output_folder)
    i=len(filepath)
    if not reset:
        json_file_path = os.path.join(Output_folder,"responses.json")
        with open(json_file_path, "w") as json_file:
            json.dump(response, json_file)
    else:
        json_file_path = os.path.join(Output_folder,f"responses_{i+1}.json")
        with open(json_file_path, "w") as json_file:
            json.dump(response, json_file)
        



