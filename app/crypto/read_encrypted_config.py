import json
from app import app_config
from app.crypto import crypto_interface

def read_config():
    with open(f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['config_files']['credential']}", 'rb') as f:
        encrypted = f.read()
    return encrypted

def decrypt_config(encrypted: bytes) -> dict:
    config_bytes = crypto_interface.decrypt(encrypted)
    config = json.loads(config_bytes)
    return config


def main():
    """
    _summary_
    """
    encrypted = read_config()
    config = decrypt_config(encrypted)
    return config

if __name__ == '__main__':
    main()