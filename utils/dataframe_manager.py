import json
import pandas as pd

from utils.pandas_filter_builder import filter_builder




def load_df_from_csv(file):
    """Loads a dataframe from a .csv file with the appropriate parameters.
    
    :param str file: Path to the CSV file to load.
    :return: A pandas DataFrame containing the loadeddata.
    :rtype: pd.DataFrame
    """
    df = pd.read_csv(file, sep = ";", date_format="%d/%m/%Y", decimal=",",  encoding="utf-8-sig", low_memory=False)
    return df

def export_df_to_csv(df, file):
    '''Export a dataframe to .csv file with the appropriate parameters

    :param pd.DataFrame df: the dataframe to be exported.
    :param str file: The file name or file path (without extension) for the resulting CSV file.
    
    The export process applies the following settings:
        - index: Excluded from the exported file.
        - encoding: UTF-8 with BOM (utf-8-sig) for compatibility with various systems.
        - date_format: Dates are formatted as "dd/mm/yyyy".
        - sep: ";" is used as the delimiter.
    '''
    df.to_csv(f"{file}.csv", index = False, encoding="utf-8-sig", date_format="%d/%m/%Y", sep = ";", decimal=",")


def filter_df_from_dict(df, filter_dict):
    """Apply a filter to a pandas DataFrame based on a dictionary.
    
    :param pd.DataFrame df: the DataFrame to be filtered.
    :param dict filter_dict: the dictionary describing the filter to apply.
    :return: the filtered DataFrame.
    :rtype: pd.DataFrame
    """
    filter = filter_builder(filter_dict)
    return df[filter(df)]

def filter_df_from_json(df, file):
    """Apply a filter to a pandas DataFrame based on a JSON configuration file.
    
    :param pd.DataFrame df: the DataFrame to be filtered.
    :param str file: Path to the JSON file describing the filter to apply.
    :return: the filtered DataFrame.
    :rtype: pd.DataFrame
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            filter_json = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in file")
   
    return  filter_df_from_dict(df, filter_json)


def filter_df_from_list(df, filters, combine = "AND"):
    """  Apply multiple boolean filters to a pandas DataFrame.

    :param pd.DataFrame df: The DataFrame to filter.
    :param list[pd.Series] filters: A list of boolean Series objects, 
                                     each representing a filter condition.
    :param str combine: Logical operator to combine the filters. Values : AND, OR. Defaults to "AND".
    :return: A filtered DataFrame containing only rows that satisfy all filters.
    :rtype: pd.DataFrame
    """
    
    if not isinstance(filters, list):
        raise TypeError("Filters must be provided as a list of pandas Series objects.")
    if not all(isinstance(f, pd.Series) for f in filters):
        raise ValueError("Each filter in the list must be a pandas Series object.")
    if not filters:
        raise ValueError("The filters list is empty. Provide at least one filter.")
    if not all(isinstance(f, pd.Series) for f in filters):
        raise ValueError("All filters must be pandas Series objects.")
    if combine.upper() not in {"AND", "OR"}:
        raise ValueError("Invalid combine parameter. Use 'AND' or 'OR' (case-insensitive).")
    

    if combine == "AND":
        mask = pd.concat(filters, axis=1).all(axis="columns")
    elif combine == "OR":
        mask = pd.concat(filters, axis=1).any(axis="columns")
    else:
        raise ValueError("Invalid combine parameter. Use 'AND' or 'OR'.")
    filtered_df = df[mask]
    
    return filtered_df

