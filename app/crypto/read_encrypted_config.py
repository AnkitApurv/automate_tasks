import json
from app import app_config, logging_config
from app.crypto import crypto_interface

def read_config(profile: dict):
    with open(f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['config_files']['credential']}", 'rb') as f:
        encrypted = f.read()
    return encrypted

def decrypt_config(encrypted: bytes) -> dict:
    config_bytes = crypto_interface.decrypt(encrypted)
    config = json.loads(config_bytes)
    return config


def main(profile: dict):
    """
    _summary_
    """
    logging_config.log.info('Read Current Credentials: Begin')
    encrypted = read_config(profile = profile)
    config = decrypt_config(encrypted = encrypted)
    logging_config.log.info('Read Current Credentials: Done')
    return config
