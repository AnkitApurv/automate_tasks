import argparse
from app import logging_config
from app.crypto import make_encrypted_config, read_encrypted_config

def update_config(config: dict) -> dict:
    """
    _summary_

    :return: _description_
    :rtype: _type_
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("password")
    config_new = parser.parse_args().__dict__
    config_updated = config | config_new # new in Python 3.9, see https://peps.python.org/pep-0584/
    return config_updated

def main():
    """
    _summary_
    """
    logging_config.log.info('Read Current Credentials: Begin')
    config_old = read_encrypted_config.main()
    logging_config.log.info('Read Current Credentials: Done')
    logging_config.log.info('Prompt User for New Password: Begin')
    config_updated = update_config(config_old)
    logging_config.log.info('Prompt User for New Password: Done')
    logging_config.log.info('Save New Credentials: Begin')
    encrypted_new = make_encrypted_config.encrypt_config(config_updated)
    make_encrypted_config.save_config(encrypted_new)
    logging_config.log.info('Save New Credentials: Done')
    return

if __name__ == '__main__':
    main()