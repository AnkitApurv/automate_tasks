import argparse

from app import logging_config
from app.manage_task_secrets.tradetron.add_credentials import encrypt_config, save_config

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
