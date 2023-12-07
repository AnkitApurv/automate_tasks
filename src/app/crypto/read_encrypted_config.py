import json
from typing import Any, Dict

from app.crypto import crypto_interface


def read_config(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        encrypted: bytes = f.read()
    return encrypted

def decrypt_config(encrypted: bytes) -> Dict[Any, Any]:
    config_bytes: bytes = crypto_interface.decrypt(encrypted)
    config: Dict[Any, Any] = json.loads(config_bytes)
    return config


def main(file_path: str) -> Dict[Any, Any]:
    """
    _summary_
    """
    encrypted: bytes = read_config(file_path = file_path)
    config: Dict[Any, Any] = decrypt_config(encrypted = encrypted)
    return config
    config: Dict[Any, Any] = decrypt_config(encrypted = encrypted)
    return config
