def update_config(config_old: dict, config_new: dict) -> dict:
    """
    _summary_

    :param config_old: _description_
    :type config_old: dict
    :param config_new: _description_
    :type config_new: dict
    :return: _description_
    :rtype: dict
    """
    config_updated = config_old | config_new # new in Python 3.9, see https://peps.python.org/pep-0584/
    return config_updated
