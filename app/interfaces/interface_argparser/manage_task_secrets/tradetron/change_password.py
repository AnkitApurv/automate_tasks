import argparse

from app import logging_config
from app.crypto import read_encrypted_config
from app.manage_task_secrets.tradetron import add_credentials
from app.manage_task_secrets.tradetron.change_password import update_config

def main():
    """
    _summary_
    """
    config_old = read_encrypted_config.main()
    logging_config.log.info('Prompt User for New Password: Begin')
    parser = argparse.ArgumentParser()
    parser.add_argument("password")
    logging_config.log.info('Prompt User for New Password: Done')
    logging_config.log.info('Save New Credentials: Begin')
    config_updated = update_config(config_old = config_old, config_new = parser.parse_args().__dict__)
    encrypted_new = add_credentials.encrypt_config(config_updated)
    add_credentials.save_config(encrypted_new)
    logging_config.log.info('Save New Credentials: Done')
    return

if __name__ == '__main__':
    main()
