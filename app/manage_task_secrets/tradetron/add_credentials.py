"""
_summary_
"""
import json

from app import app_config
from app.crypto import crypto_interface

def encrypt_config(config: dict) -> bytes:
    """
    _summary_

    :param config: _description_
    :type config: dict
    :return: _description_
    :rtype: bytes
    """
    config_json = json.dumps(config)
    # do not use encode, it mangles original data
    config_bytes = bytes(str(config_json), encoding = 'utf-8')
    encrypted = crypto_interface.encrypt(config_bytes)
    return encrypted

def save_config(encrypted: bytes):
    """
    _summary_

    :param encrypted: _description_
    :type encrypted: bytes
    """
    with open(
        f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['config_files']['credential']}",
        'wb'
    ) as f:
        f.write(encrypted)
    return
