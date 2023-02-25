from typing import Tuple
from app import app_utils

def read_app_config(config_path: str = './app/config') -> Tuple[dict, dict]:
    paths = app_utils.read_config(file_path = f"{config_path}/paths.json")
    automation_services = app_utils.read_config(file_path = f"{paths['config']}/automation_services.json")
    return paths, automation_services

if not hasattr(__spec__, 'paths'):
    paths, automation_services = read_app_config()