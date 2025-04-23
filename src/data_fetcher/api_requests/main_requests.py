from src.data_fetcher.api_requests.journeys_request_handler import batch_journeys_calculation
from utils.datetime_manager import format_datetime
from utils.env_manager import get_env_var


def process(ref_point, endpoint_df, journey_config, go_params=None, return_params=None):
    """
    Processes journey calculations using reference points, endpoints, and configurations.
    The function triggers batch calculations and saves results.

    :param dict ref_point: Dictionary containing reference point 'latitude' and 'longitude'.
    :param pd.DataFrame endpoint_df: DataFrame with endpoint locations ('id', 'latitude' and 'longitude').
    :param dict journey_config: Configuration dictionary for journey calculations.
    :param dict go_params: Dictionary containing folders and datetime for 'go' journeys (default: None).
    Expected keys:
            - 'result_folder': Path where successful journey results will be saved.
            - 'failed_folder': Path where failed journey results will be saved.
            - 'datetime' : datetime of the journey
    :param dict return_params: Dictionary containing folders and datetime for 'return' journeys (default: None).
    Expected keys :
        Same than go_params
    :rtype: None
    :return: No return value; the function triggers batch calculations and saves results.
    """
    try:
        apiToken = get_env_var("API_TOKEN")
    except ValueError as e:
        raise Exception from e

    if go_params:
         go_folders = {
        'result_folder': go_params['result_folder'],
        'failed_folder': go_params['failed_folder']
        }
         batch_journeys_calculation(ref_point, 
                            endpoint_df,
                            {**journey_config, 'datetime': go_params['datetime']},
                            apiToken,
                            go_folders,
                            )
    if return_params:
        return_folders = {
        'result_folder': return_params['result_folder'],
        'failed_folder': return_params['failed_folder']
        }
        
        batch_journeys_calculation(ref_point, 
                            endpoint_df,
                            {**journey_config, 'datetime': return_params['datetime']},
                            apiToken,
                            return_folders,
                            from_ref_to_endpoints=False)