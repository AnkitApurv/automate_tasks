import logging
import secrets

import pywebio
import pywebio_battery

from app import app_config, logging_utils
from app.crypto import read_encrypted_config
from app.manage_tasks_config.tradetron import create_task, auth_user

logger: logging.Logger = logging.Logger(app_config.services['tradetron']['name'])
logging_extra_info: logging_utils.LoggingExtraInfo = {'service': app_config.services['tradetron']['name'], 'task': 'generic'}

task_config: dict = {}

def verify_login() -> str | None:
    username: str | None = None
    credentials_provided = pywebio.input.input_group(
        label = 'Verify Credentials',
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
    credentials_stored = read_encrypted_config.main(file_path = task_config['files']['credentials'])
    if auth_user.verify_login(received_credentials = credentials_provided, stored_credentials = credentials_stored)
        username = credentials_stored['username']
    return username

def main():
    """
    _summary_
    """
    logger.info('Get Task Name: Begin', extra = logging_extra_info)
    task_name = pywebio.input.input_group(
        label = 'Tradetron',
        inputs = [
            pywebio.input.input(
                label = 'Task Name', placeholder = 'tradetron_abcd', help_text = "What's your Tradetron Task's Name?",
                type = pywebio.input.TEXT, name = 'task_name',required = True
            )
        ]
    )
    if app_config.tasks.get(task_name, None) is None:
        logger.warning('Task does not exist!')
        exit(0) # change this, it's a web app
    logging_extra_info['task'] = task_name['task_name']
    task_config = app_config.tasks[task_name['task_name']]
    logger.info('Get Task Name: Done', extra = logging_extra_info)

    logger.info('Authenticate User: Begin', extra = logging_extra_info)
    hmac_secret = secrets.token_bytes(nbytes = 256)
    username = pywebio_battery.custom_auth(
        login_func = verify_login,
        secret = hmac_secret,
    )
    logger.info('Authenticate User: Done', extra = logging_extra_info)
    
    logger.info('Prompt User for New Password: Begin', extra = logging_extra_info)
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
    logger.info('Prompt User for New Password: Done', extra = logging_extra_info)
    
    logger.info('Save New Credentials: Begin', extra = logging_extra_info)
    credentials_current = read_encrypted_config.main(file_path = task_config['files']['credentials'])
    credentials_updated = credentials_current | new_passwd
    create_task.save_credentials(credentials = credentials_updated, file_path = task_config['files']['credentials'])
    logger.info('Save New Credentials: Done', extra = logging_extra_info)

    logger.info('De-auth User: Begin', extra = logging_extra_info)
    pywebio_battery.revoke_auth()
    logger.info('De-auth User: Done', extra = logging_extra_info)
    
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
