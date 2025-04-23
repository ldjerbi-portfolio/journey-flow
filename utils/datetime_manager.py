from datetime import datetime


def sec_to_min(time_in_seconds):
    """Convert seconds to minutes.
    :rtype: str
    """
    return round(time_in_seconds/60,2)

def sec_to_min_str(time_in_seconds):
    """Convert seconds to minutes and return as string.
    :rtype: str
    """
    return str(sec_to_min(time_in_seconds))



def format_datetime(datetime_string = None, target_format = "%Y%m%dT%H%M%S", source_format ="%d/%m/%Y %H:%M:%S"):
    """Formats a given date string into a specified output format.

    :param str datetime_string: Date as a string (e.g., "01/01/2025 18:30:00").
                       If None, defaults to the current datetime.
    :param str target_format: Desired format for the output string (default: "%Y%m%dT%H%M%S").
    :param str source_format: Format of the input date string (default: "%d/%m/%Y %H:%M:%S").
    :return: Formatted date string.
    
    Example Usage:
    >>> format_datetime("01/01/2025 18:30:00", "%Y-%m-%d %H:%M:%S", inputFormat = "%d/%m/%Y %H:%M:%S")
    '2025-01-01 18:30:00'

    >>> format_datetime(target_format="%d/%m/%Y %Hh%M%S")
    "01/01/2025 18:30:00"  # Uses current date
    """
    d = datetime.now() if datetime_string is None else datetime.strptime(datetime_string, source_format)
    return d.strftime(target_format)



        