import json


def read_config(config_path):
    """
    Reads the configuration JSON file.

    Args:
    - config_path (str): Path to the configuration JSON file.

    Returns:
    - dict: Parsed JSON configuration.
    """
    with open(config_path, "r") as file:
        return json.load(file)
