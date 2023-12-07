import logging

import pywebio

from app import app_config, logging_utils
from app.manage_tasks_config.tradetron import create_task, tradetron_utils

logger: logging.Logger = logging.Logger(app_config.services['tradetron']['name'])
logging_extra_info: logging_utils.LoggingExtraInfo = {'service': app_config.services['tradetron']['name'], 'task': 'generic'}

def main():
    """
    _summary_
    """
    logger.info('Prompt User for New Task Name: Begin', extra = logging_extra_info)
    task_name = pywebio.input.input_group(
        label = 'New Task',
        inputs = [
            pywebio.input.input(
                label = 'Task Name', placeholder = 'task_name', help_text = "It could be any random phrase by way of which you could remember this task.",
                type = pywebio.input.TEXT, name = 'task_name', required = True
            )
        ]
    )
    logger.info('Prompt User for New Task Name: Done', extra = logging_extra_info)

    logger.info('Prompt User for Credentials: Begin', extra = logging_extra_info)
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
    credentials = tradetron_utils.Credentials(
        username = credentials['username'],
        password = credentials['password'],
        otp = credentials['otp']
    )
    logger.info('Prompt User for Credentials: Done', extra = logging_extra_info)

    logger.info('Register New Task: Begin', extra = logging_extra_info)
    create_task.main(task_name = task_name['task_name'], credentials = credentials)
    logger.info('Register New Task: Done', extra = logging_extra_info)

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