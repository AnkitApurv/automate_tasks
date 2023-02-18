import json

def read_config(config_file_path: str) -> dict:
    """
    _summary_

    :param config_file_path: _description_
    :type config_file_path: str
    :return: _description_
    :rtype: dict
    """
    with open(file = config_file_path, mode = 'rt', encoding = 'utf8') as f:
        config = json.loads(s = f.read())
    return config