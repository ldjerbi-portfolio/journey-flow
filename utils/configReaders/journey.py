
import json


def exportConfig(config, filePath):
    """
    Exports a configuration dictionary to a JSON file.

    :param config: Dictionary containing configuration data.
    :param filePath: Full path where the file should be saved.
    """
    directory = os.path.dirname(filePath)
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Ensure file has correct extension
    if not filePath.endswith(".json"):
        raise ValueError("File extension must be .json")

    with open(filePath, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def importConfig(filePath):
   """
    Imports a configuration dictionary from a JSON file.

    :param filePath: Full path to the JSON file.
    :return: Dictionary containing configuration data.
    """
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"Configuration file not found: {filePath}")

    if not filePath.endswith(".json"):
        raise ValueError("File extension must be .json")

    with open(filePath, "r", encoding="utf-8") as f:
        return json.load(f)


