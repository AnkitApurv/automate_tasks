import pywebio

from app import logging_config
from app.manage_task_secrets.tradetron.add_credentials import encrypt_config, save_config

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