from utils.dataframe_manager import filter_df_from_json, load_df_from_csv

def process(df_file, filter_file = None, filter_dict = None):
    """
    Load a CSV file into a DataFrame, optionally filtering it using a JSON file.

    :param str df_file: Path to the CSV file to be loaded into a DataFrame.
    :param str filter_file: Path to the JSON file containing filter conditions (default is None).
    
    :return: Processed DataFrame with lowercase column names, optionally filtered.
    :rtype: pd.DataFrame
    """
    df = load_df_from_csv(df_file)
    
    if filter_file:
       df = filter_df_from_json(df, filter_file)
   
    df.columns = df.columns.str.lower()
    
    return df