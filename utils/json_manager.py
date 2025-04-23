import json

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

