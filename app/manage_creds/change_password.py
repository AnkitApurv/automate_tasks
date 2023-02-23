import argparse
import pywebio
import pywebio_battery

from app import logging_config
from app.crypto import read_encrypted_config
from app.manage_creds import add_credentials, auth_user_pywebio

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

def main_pywebio():
    """
    _summary_
    """
    config_old = read_encrypted_config.main()
    logging_config.log.info('Authenticate User: Begin')
    username = pywebio_battery.basic_auth(
        verify_func = auth_user_pywebio.verify_login,
        secret = 'jfvbs asa< eflwdjocbfverje439ry4r98jcipmwd,q3',
    )
    logging_config.log.info('Authenticate User: Done')
    logging_config.log.info('Prompt User for New Password: Begin')
    pywebio.output.put_text("Welcome, %s!" % username)
    new_passwd = pywebio.input.input_group(
        label = 'Update Credentials',
        inputs = [
            pywebio.input.input(
                label = 'New Password', placeholder = 'new_password', help_text = "What's your new password?",
                type = pywebio.input.PASSWORD, name = 'password',required = True
            )
        ]
    )
    logging_config.log.info('Prompt User for New Password: Done')
    logging_config.log.info('De-auth User: Begin')
    pywebio_battery.revoke_auth()
    logging_config.log.info('De-auth User: Done')
    logging_config.log.info('Save New Credentials: Begin')
    config_updated = update_config(config_old = config_old, config_new = new_passwd)
    encrypted_new = add_credentials.encrypt_config(config_updated)
    add_credentials.save_config(encrypted_new)
    logging_config.log.info('Save New Credentials: Done')
    pywebio.output.put_grid(
        content = [
            [pywebio.output.put_markdown("# Credentials updated!")],
            [pywebio.output.put_markdown("## Available Options")],
            [
                pywebio.output.put_markdown("### Return to landing page"),
                pywebio.output.put_link(name = 'Return to landing page', url = '/')
            ],
        ]
    )
    return

def main_argparser():
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
    main_argparser()