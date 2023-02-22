"""
_summary_
"""
from typing import Tuple, Any
import time

import docker

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
    website_config = app_utils.read_config(
        config_file_path = f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['config_files']['webpage']}"
    )
    url = website_config['url']
    username_id = website_config['username_id']
    password_id = website_config['password_id']
    otp_id = website_config['otp_id']
    submit_button_id = website_config['submit_button_id']
    return url, username_id, password_id, otp_id, submit_button_id

def run_container():
    """
    _summary_
    """
    return docker.from_env().containers.run(
        image = 'selenium/standalone-chrome', shm_size = '2g',
        detach = True, remove = True, auto_remove = True,
        publish_all_ports = True
    )

def instantiate_driver(exposed_ports: dict) -> webdriver.Remote:
    """
    _summary_

    :return: _description_
    :rtype: webdriver.Remote
    """
    browser_options = Browser_Options()
    browser_options.add_argument('--headless')
    browser_options.add_argument('--disable-extensions')
    browser_options.add_argument('--disable-gpu')

    selenium_port_container = '4444/tcp'
    selenium_port_host: str = exposed_ports[selenium_port_container] \
        if len(exposed_ports[selenium_port_container]) > 0 \
        else \
            selenium_port_container[:-4]

    return webdriver.Remote(
        command_executor = f"http://127.0.0.1:{selenium_port_host}/wd/hub",
        options = browser_options
    )

def setup() -> Tuple[webdriver.Remote, Any]:
    """
    _summary_

    :return: _description_
    :rtype: _type_
    """
    browser_container = run_container()
    driver = instantiate_driver(exposed_ports = browser_container.attrs['Config']['ExposedPorts'])
    return driver, browser_container

def login(
    driver: webdriver.Remote, url: str,
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
    driver.get(url)
    # giving time for webpage to load,
    # inefficient but no optimal solution available
    time.sleep(3)

    driver.save_screenshot('./scheduled_login_tradetron/logs/1_before_form_fill.png')
    driver.find_element(Find_Element_By.ID, username_id).send_keys(username)
    driver.find_element(Find_Element_By.ID, password_id).send_keys(password)
    driver.find_element(Find_Element_By.ID, otp_id).send_keys(otp)
    WebDriverWait(driver = driver, timeout = 3).until(
        expected_conditions.text_to_be_present_in_element_value(
            (Find_Element_By.ID, otp_id), otp
        )
    )
    # giving time for form filling to be completed successfully,
    # inefficient but no optimal solution available
    time.sleep(1)
    driver.save_screenshot('./scheduled_login_tradetron/logs/2_after_form_fill.png')
    driver.find_element(Find_Element_By.ID, submit_button_id).click()
    driver.save_screenshot('./scheduled_login_tradetron/logs/3_after_form_submit.png')
    WebDriverWait(driver = driver, timeout = 15).until(
        expected_conditions.title_is('Success')
    )
    driver.save_screenshot('./scheduled_login_tradetron/logs/4_after_redirect.png')
    return

def teardown_driver(driver: webdriver.Remote):
    """
    _summary_

    :param driver: _description_
    :type driver: webdriver.Remote
    """
    driver.quit()
    return

def teardown_container(browser_container):
    """
    _summary_
    """
    with open(f"{app_config.config_paths['logs_base_path']}/container_log.log", 'wb') as container_log:
        container_log.write(
            browser_container.logs(
                stream = False, timestamps = True, tail = 'all', follow = None
            )
        )
    browser_container.stop()
    # container will be removed automatically once stopped, owing to it's run config
    return

def teardown(driver: webdriver.Remote, browser_container):
    """
    _summary_

    :param driver: _description_
    :type driver: webdriver.Remote
    """
    teardown_driver(driver = driver)
    teardown_container(browser_container = browser_container)
    return

def main():
    """
    _summary_
    """
    username, password, otp = read_credential()
    logging_config.log.info('Read Website Configuration: Begin')
    url, username_id, password_id, otp_id, submit_button_id = read_website_config()
    logging_config.log.info('Read Website Configuration: Done')
    logging_config.log.info('Instantiate Web Browser: Begin')
    driver, browser_container = setup()
    logging_config.log.info('Container ID: %s', browser_container.id)
    logging_config.log.info('Container Name: %s', browser_container.name)
    logging_config.log.info('Instantiate Web Browser: Done')
    logging_config.log.info('Logging In: Begin')
    login(
        driver = driver,
        url = url,
        username_id = username_id, username = username,
        password_id = password_id, password = password,
        otp_id = otp_id, otp = otp,
        submit_button_id = submit_button_id
    )
    logging_config.log.info('Logging In: Done')
    logging_config.log.info('Teardown: Begin')
    teardown(driver = driver, browser_container = browser_container)
    logging_config.log.info('Teardown: Done')
    return

if __name__ == '__main__':
    main()
