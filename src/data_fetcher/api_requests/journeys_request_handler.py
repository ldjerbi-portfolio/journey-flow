import json
import os
import requests


def fetch_journey(from_position, to_position, journey_params, api_token):
    """
    Fetches journey data between two positions using PRIM API.

    :param dict from_position: A dictionary containing the starting position with 'latitude' and 'longitude'.
    :param dict to_position: A dictionary containing the destination position with 'latitude' and 'longitude'.
    :param dict journey_params: A dictionary containing additional parameters for the journey request.
    :param str api_token: The API token required for authentication with the API.
    
    :return: A tuple containing the HTTP response status code and the JSON data from the API response.
    :rtype: tuple(int, dict)
    """
        
    #Preparing the requests
    url = "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/journeys"
    
    headers = {
        'apikey': api_token,  
    }
    
    params = {
        'from': f"{from_position['longitude']};{from_position['latitude']}", 
        'to' : f"{to_position['longitude']};{to_position['latitude']}",
        
        **journey_params
    }
   
    #Requesting
    response = requests.get(url, headers=headers, params=params)

    try:
        data = response.json()
    except ValueError:
        data = {"error": "Réponse non valide."}
    return response.status_code, data

        

def batch_journeys_calculation(ref_position, journey_endpoints, 
                              journey_param, api_token, 
                              output_folders, from_ref_to_endpoints=True):
    """
    Batch calculates journeys between a reference position and multiple endpoints,
    storing the results in the appropriate output folders.

    :param dict ref_position: A dictionary containing the reference position with 'latitude' and 'longitude'.
    :param pandas.DataFrame journey_endpoints: A DataFrame where each row represents an endpoint with at least an 'id', 'latitude' and 'longitude'.
    :param dict journey_param: A dictionary containing parameters required for journey calculation.
    :param str api_token: A string containing the API token used for authentication with the journey API.
    :param dict output_folders: A dictionary containing paths for the result and failed journey folders.
        Expected keys:
            - 'result_folder': Path where successful journey results will be saved.
            - 'failed_folder': Path where failed journey results will be saved.
    :param bool from_ref_to_endpoints: If True (default), calculates journeys from the reference position to the endpoints.
        If False, calculates journeys from the endpoints to the reference position.
    :return: None

    Files Created:
    --------------
    - Successful journeys are saved as JSON files named <endpoint_Id>.json in `result_folder`.
    - Failed journeys are saved as JSON files named <error_code>_<endpoint_Id>.json in `failed_folder`.

   
    """

    #creating folder to save results
    os.makedirs(output_folders['result_folder'], exist_ok=True)
    os.makedirs(output_folders['failed_folder'], exist_ok=True)


    #getting journeys from API
    for index,endpoint in journey_endpoints.iterrows():
        endpointPosition = {
            'longitude': endpoint['longitude'],
            'latitude': endpoint['latitude']
        }

        if from_ref_to_endpoints:
            code, data = fetch_journey(ref_position, endpointPosition, journey_param, api_token)
        else:
            code, data = fetch_journey(endpointPosition, ref_position, journey_param, api_token)
        
        filename = endpoint['id']
        #Getting the result and storing it ine the appropriate file
        if code == 200:
            file_path = os.path.join(output_folders['result_folder'], f"{filename}.json")
        else:
            file_path = os.path.join(output_folders['failed_folder'], f"{code}_{filename}.json")
            
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
