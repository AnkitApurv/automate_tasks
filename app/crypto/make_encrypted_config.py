import json
import argparse
from app import app_config, logging_config
from app.crypto import crypto_interface

def get_config():
    """
    _summary_

    :return: _description_
    :rtype: _type_
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("otp")
    config = parser.parse_args().__dict__
    return config

def encrypt_config(config: dict) -> bytes:
    """
    _summary_

    :param config: _description_
    :type config: dict
    :return: _description_
    :rtype: bytes
    """
    config_json = json.dumps(config)
    config_bytes = bytes(str(config_json), encoding = 'utf-8') # do not use encode, it mangles original data
    encrypted = crypto_interface.encrypt(config_bytes)
    return encrypted

def save_config(encrypted: bytes):
    """
    _summary_

    :param encrypted: _description_
    :type encrypted: bytes
    """
    with open(f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['config_files']['credential']}", 'wb') as f:
        f.write(encrypted)
    return


def main():
    """
    _summary_
    """
    logging_config.log.info('Prompt User for Credentials: Begin')
    config = get_config()
    logging_config.log.info('Prompt User for Credentials: Done')
    logging_config.log.info('Save New Credentials: Begin')
    encrypted = encrypt_config(config)
    save_config(encrypted)
    logging_config.log.info('Save New Credentials: Done')
    return

if __name__ == '__main__':
    main()