from typing import Tuple
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as Browser_Options
from selenium.webdriver.common.by import By as Find_Element_By

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
    website_config = app_utils.read_config(config_file_path = f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['config_files']['webpage']}")
    url = website_config['url']
    username_id = website_config['username_id']
    password_id = website_config['password_id']
    otp_id = website_config['otp_id']
    submit_button_id = website_config['submit_button_id']
    return url, username_id, password_id, otp_id, submit_button_id


def login(url: str, username_id: str, username: str, password_id: str, password: str, otp_id: str, otp: str,submit_button_id: str):
    """
    _summary_

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
    browser_options = Browser_Options()
    browser_options.add_argument("--headless")
    browser_options.add_argument("--disable-extensions")
    browser_options.add_argument("--disable-gpu")

    browser = webdriver.Chrome()

    browser.get(url)
    time.sleep(5) # giving time for webpage to load, inefficient but no optimal solution available

    browser.save_screenshot('./scheduled_login_tradetron/logs/before_form_fill.png')
    browser.find_element(Find_Element_By.ID, username_id).send_keys(username)
    browser.find_element(Find_Element_By.ID, password_id).send_keys(password)
    browser.find_element(Find_Element_By.ID, otp_id).send_keys(otp)
    WebDriverWait(driver = browser, timeout = 5).until(
        expected_conditions.text_to_be_present_in_element_value(
            (Find_Element_By.ID, otp_id), otp
        )
    )
    time.sleep(5) # giving time for form filling to be completed successfully inefficient but no optimal solution available
    browser.save_screenshot('./scheduled_login_tradetron/logs/after_form_fill.png')
    browser.find_element(Find_Element_By.ID, submit_button_id).click()
    browser.save_screenshot('./scheduled_login_tradetron/logs/after_form_submit.png')
    WebDriverWait(driver = browser, timeout = 5).until(
        expected_conditions.title_is('Success')
    )
    browser.save_screenshot('./scheduled_login_tradetron/logs/after_redirect.png')
    browser.quit()
    return

def main():
    """
    _summary_
    """
    username, password, otp = read_credential()
    logging_config.log.info('Read Website Configuration: Begin')
    url, username_id, password_id, otp_id, submit_button_id = read_website_config()
    logging_config.log.info('Read Website Configuration: Done')
    logging_config.log.info('Logging In: Begin')
    login(
        url = url,
        username_id = username_id, username = username,
        password_id = password_id, password = password,
        otp_id = otp_id, otp = otp,
        submit_button_id = submit_button_id
    )
    logging_config.log.info('Logging In: Done')
    return

if __name__ == '__main__':
    main()
