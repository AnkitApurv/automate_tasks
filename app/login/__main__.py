"""
_summary_
"""
from typing import Tuple

from playwright import sync_api

from app import app_utils, app_config, logging_config
from app.crypto import read_encrypted_config

def read_credential() -> Tuple[str, str, str]:
    """
    _summary_

    :return: _description_
    :rtype: Tuple[str, str, str]
    """

    credentials = read_encrypted_config.main()
    username = credentials['username']
    password = credentials['password']
    otp = credentials['otp']
    return username, password, otp

def read_website_config() -> Tuple[str, str, str, str, str]:
    """
    _summary_

    :return: _description_
    :rtype: Tuple[str, str, str, str, str]
    """
    logging_config.log.info('Read Website Configuration: Begin')
    website_config = app_utils.read_config(
        config_file_path = f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['config_files']['webpage']}"
    )
    url = website_config['url']
    username_id = website_config['username_id']
    password_id = website_config['password_id']
    otp_id = website_config['otp_id']
    submit_button_id = website_config['submit_button_id']
    logging_config.log.info('Read Website Configuration: Done')
    return url, username_id, password_id, otp_id, submit_button_id

def login(url: str,
    username_id: str, username: str,
    password_id: str, password: str,
    otp_id: str, otp: str,
    submit_button_id: str):
    """
    _summary_

    :param driver: _description_
    :type driver: webdriver.Remote
    :param url: _description_
    :type url: str
    :param username_id: _description_
    :type username_id: str
    :param username: _description_
    :type username: str
    :param password_id: _description_
    :type password_id: str
    :param password: _description_
    :type password: str
    :param otp_id: _description_
    :type otp_id: str
    :param otp: _description_
    :type otp: str
    :param submit_button_id: _description_
    :type submit_button_id: str
    """
    logging_config.log.info('Instantiate Web Browser: Begin')
    with sync_api.sync_playwright() as p:
        browser = p.firefox.launch(headless = True, slow_mo = 50)
        page = browser.new_page()
        logging_config.log.info('Instantiate Web Browser: Done')
        logging_config.log.info('Logging In: Begin')
        page.goto(url = url)
        page.screenshot(path = f"{app_config.config_paths['logs_base_path']}/1_before_form_fill.png")
        page.get_by_label(username_id).fill(username)
        page.get_by_label(password_id).fill(password)
        page.get_by_label(otp_id).fill(otp)
        page.screenshot(path = f"{app_config.config_paths['logs_base_path']}/2_after_form_fill.png")
        page.get_by_role(role = 'button', name = submit_button_id).click(button = 'left', delay = 50)
        page.screenshot(path = f"{app_config.config_paths['logs_base_path']}/3_after_form_submit.png")
        with page.expect_navigation(wait_until='load'):
            sync_api.expect(page).to_have_title('Success')
        page.screenshot(path = f"{app_config.config_paths['logs_base_path']}/4_after_redirect.png")
        logging_config.log.info('Logging In: Done')
        browser.close()
    return

def main():
    """
    _summary_
    """
    username, password, otp = read_credential()
    url, username_id, password_id, otp_id, submit_button_id = read_website_config()
    login(
        url = url,
        username_id = username_id, username = username,
        password_id = password_id, password = password,
        otp_id = otp_id, otp = otp,
        submit_button_id = submit_button_id
    )
    return

if __name__ == '__main__':
    main()
