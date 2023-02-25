import pywebio
import pywebio_battery

from app import logging_config
from app.crypto import read_encrypted_config
from app.manage_task_secrets.tradetron import add_credentials
from app.manage_task_secrets.tradetron.change_password import update_config
from app.interfaces.interface_pywebio.manage_task_secrets.tradetron import auth_user

def main_pywebio():
    """
    _summary_
    """
    config_old = read_encrypted_config.main()
    logging_config.log.info('Authenticate User: Begin')
    username = pywebio_battery.basic_auth(
        verify_func = auth_user.verify_login,
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