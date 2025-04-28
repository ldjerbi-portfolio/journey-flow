import json
import os

def export_json(data, file):
    """
    Exports data to a JSON file with UTF-8 encoding and proper formatting.
    
    :param data: The data to be exported (must be JSON serializable).
    :param str file: The file path where data will be saved.
    """
    with open(file, "w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def import_json(file):
    """
    Imports data from a JSON file with UTF-8 encoding.
    
    :param str file: The file path from where data will be loaded.
    :return: The deserialized data from the JSON file.
    :rtype: dict or list
    """
    with open(file, "r", encoding="utf-8-sig") as f:
        data = json.load(f)  
    return data

def load_json_from_folder(folder_path, recursive = False):
    """Loads all JSON files from a specified folder and returns their contents as a list of dictionaries.
    
    :param str folder_path: The path to the folder containing JSON files.
    :param bool recursive: If True, the function will scan subfolders recursively.
    :return: A list of dictionaries, each representing the contents of a JSON file.
    :rtype: list
    """
    json_data = []
    subfolders = []

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        if recursive and os.path.isdir(full_path):
            subfolders.append(full_path)

        if filename.endswith(".json"):
            base_name, _ = os.path.splitext(filename)
            with open(full_path, mode = "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            json_data.append({
                'id' : base_name,
                'folder' : folder_path,
                **data
            })
        
    if recursive:
        for subfolder in subfolders:
            json_data.extend(load_json_from_folder(subfolder, recursive))

    return json_data
