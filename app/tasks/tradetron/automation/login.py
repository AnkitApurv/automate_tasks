"""
_summary_
"""
import logging
from sys import argv, exit
from typing import Any, Dict

from playwright import sync_api
from playwright.sync_api import Browser, Page

from app import app_config, app_utils, logging_utils
from app.crypto import read_encrypted_config
from app.tasks.tradetron.manage_tasks.tradetron_utils import (Credentials,
                                                              WebSiteConfig)

logger: logging.Logger = logging.Logger(app_config.services['tradetron']['name'])
logging_extra_info: logging_utils.LoggingExtraInfo = {'service': app_config.services['tradetron']['name'], 'task': 'generic'}

def read_credential(task_config: Dict[Any, Any]) -> Credentials:
    """
    _summary_

    :param task_config: _description_
    :type task_config: dict
    :return: _description_
    :rtype: Credentials
    """
    credentials: Dict[Any, Any] = read_encrypted_config.main(file_path = task_config['files']['credentials'])
    return Credentials(**credentials)

def read_website_config(service_config: Dict[Any, Any]) -> WebSiteConfig:
    """
    _summary_

    :param service_config: _description_
    :type service_config: dict
    :return: _description_
    :rtype: WebSiteConfig
    """
    logger.info('Read Website Configuration: Begin', extra = logging_extra_info)
    website_config: Dict[Any, Any] = app_utils.read_config(
        file_path = f"{service_config['config_path']}/website.yaml"
    )
    logger.info('Read Website Configuration: Done', extra = logging_extra_info)
    return WebSiteConfig(**website_config)

def login(website_config: WebSiteConfig, credentials: Credentials, service_config: Dict[Any, Any], task_config: Dict[Any, Any]) -> None:
    """
    _summary_

    :param website_config: _description_
    :type website_config: WebSiteConfig
    :param credentials: _description_
    :type credentials: Credentials
    :param service_config: _description_
    :type service_config: dict
    """
    logger.info('Instantiate Web Browser: Begin', extra = logging_extra_info)
    with sync_api.sync_playwright() as p:
        browser: Browser = p.firefox.launch(headless = True, slow_mo = 50)
        page: Page = browser.new_page()
        logger.info('Instantiate Web Browser: Done', extra = logging_extra_info)

        logger.info('Logging In: Begin', extra = logging_extra_info)

        page.goto(url = website_config['url'])
        page.screenshot(path = f"{service_config['log_path']}/1_before_form_fill_{task_config['name']}.png")

        page.get_by_label(website_config['username_id']).fill(credentials['username'])
        page.get_by_label(website_config['password_id']).fill(credentials['password'])
        page.get_by_label(website_config['otp_id']).fill(credentials['otp'])
        page.screenshot(path = f"{service_config['log_path']}/2_after_form_fill_{task_config['name']}.png")

        page.get_by_role(role = 'button', name = website_config['submit_button_id']).click(button = 'left', delay = 50)
        page.screenshot(path = f"{service_config['log_path']}/3_after_form_submit_{task_config['name']}.png")

        with page.expect_navigation(wait_until='load'):
            sync_api.expect(page).to_have_title('Success')
        page.screenshot(path = f"{service_config['log_path']}/4_after_redirect_{task_config['name']}.png")
        logger.info('Logging In: Done', extra = logging_extra_info)
        
        browser.close()
    return

def main(task_name: str) -> None:
    """
    _summary_

    :param task_config: _description_
    :type task_config: dict
    :param service_config: _description_, defaults to app_config.services['tradetron']
    :type service_config: dict, optional
    """
    if app_config.tasks.get(task_name, None) is None:
        logger.warning('Task named %s not found!' % task_name)
        exit(0)

    task_config: Dict[Any, Any] = app_config.tasks[task_name]
    logging_extra_info['task'] = task_config['name']

    service_config: Dict[Any, Any] = app_config.services['tradetron']

    credentials: Credentials = read_credential(task_config = task_config)
    website_config: WebSiteConfig = read_website_config(service_config = service_config)
    login(
        website_config = website_config, credentials = credentials, 
        service_config = service_config, task_config = task_config
    )
    return


if __name__ == '__main__':
    if len(argv) > 1:
        main(argv[1])
    else:
        logger.warning('Task Name not provided!')
        exit(0)
        