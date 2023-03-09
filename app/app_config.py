import logging
import logging.config
from typing import Any, Dict, Tuple

# from systemd.journal import JournalHandler
from app import app_utils


def read_app_config(config_path: str = './app/config') -> Tuple[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]:
    paths: Dict[Any, Any] = app_utils.read_config(file_path = f"{config_path}/paths.yaml")
    services: Dict[Any, Any] = app_utils.read_config(file_path = f"{paths['app_config']}/services.yaml")
    tasks: Dict[Any, Any] = app_utils.read_config(file_path = f"{paths['profile']}/tasks.yaml")
    return paths, services, tasks

if not hasattr(__spec__, 'paths'): # module has not been imported yet
    paths, services, tasks = read_app_config()
    
    logging.config.dictConfig(
        app_utils.read_config(file_path = f"{paths['app_config']}/logging.yaml")
    )
