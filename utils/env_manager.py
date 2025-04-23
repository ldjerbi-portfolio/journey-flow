
import os


def get_env_var(varName):
    """Retrieve the value of an environment variable.
    
    :param str varName: Name of the environment variable.
    :return: Value of the environment variable.
    :rtype: str
    :raises ValueError: If the variable is missing or not loaded.
    """
    
    value = os.getenv(varName)
    if not value:
        raise ValueError(f"'{varName}' environment variable is missing. Also, check if loaded.")
    return value
