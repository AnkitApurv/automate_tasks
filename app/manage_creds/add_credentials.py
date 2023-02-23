import json
import argparse
import pywebio

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

def main_pywebio():
    """
    _summary_
    """
    logging_config.log.info('Prompt User for Credentials: Begin')
    credentials = pywebio.input.input_group(
        label = 'New Credentials',
        inputs = [
            pywebio.input.input(
                label = 'Username', placeholder = 'username', help_text = "What's your username?",
                type = pywebio.input.TEXT, name = 'username', required = True
            ),
            pywebio.input.input(
                label = 'New Password', placeholder = 'password', help_text = "What's your password?",
                type = pywebio.input.PASSWORD, name = 'password', required = True
            ),
            pywebio.input.input(
                label = 'TOTP/OTP', placeholder = 'totp/otp', help_text = "What's your otp?",
                type = pywebio.input.PASSWORD, name = 'otp', required = True
            ),
        ]
    )
    logging_config.log.info('Prompt User for Credentials: Done')
    logging_config.log.info('Save New Credentials: Begin')
    encrypted = encrypt_config(credentials)
    save_config(encrypted)
    logging_config.log.info('Save New Credentials: Done')
    pywebio.output.put_grid(
        content = [
            [pywebio.output.put_markdown("# Credentials added!")],
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
    logging_config.log.info('Prompt User for Credentials: Begin')
    config = get_config()
    logging_config.log.info('Prompt User for Credentials: Done')
    logging_config.log.info('Save New Credentials: Begin')
    encrypted = encrypt_config(config)
    save_config(encrypted)
    logging_config.log.info('Save New Credentials: Done')
    return

if __name__ == '__main__':
    main_argparser()