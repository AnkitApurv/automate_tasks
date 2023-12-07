"""
_summary_
"""
import json
from typing import Any, Dict

from app.crypto import crypto_interface


def encrypt_config(config: Dict[Any, Any]) -> bytes:
    """
    _summary_

    :param config: _description_
    :type config: dict
    :return: _description_
    :rtype: bytes
    """
    config_json: str = json.dumps(config)
    # do not use encode, it mangles original data
    config_bytes: bytes = bytes(config_json, encoding = 'utf-8')
    encrypted: bytes = crypto_interface.encrypt(config_bytes)
    return encrypted

def save_config(encrypted: bytes, file_path: str) -> None:
    """
    _summary_

    :param encrypted: _description_
    :type encrypted: bytes
    """
    with open(file_path, 'wb') as f:
        f.write(encrypted)
    return

def main(config: Dict[Any, Any], file_path: str) -> None:
    encrypted: bytes = encrypt_config(config = config)
    save_config(encrypted = encrypted, file_path = file_path)
    return
