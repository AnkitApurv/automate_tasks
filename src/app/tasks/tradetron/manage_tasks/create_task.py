"""
Necessary Steps:
1. Write profile config in tasks.yaml
2. Save credentials
3. Systemd setup:
    a. Create a copy of systemd timer for this specific task
    b. place the timer at requisite location
    c. enable timer
"""
import subprocess
from typing import Any, Dict

from app import app_config, app_utils
from app.crypto import write_encrypted_config
from app.tasks.tradetron.manage_tasks.tradetron_utils import (
    Credentials,
    TradetronTaskConfig,
    TradetronTaskConfigFiles,
)


def create_task_config(task_name: str) -> TradetronTaskConfig:
    task_config: TradetronTaskConfig = TradetronTaskConfig(
        name = task_name,
        profile_path = f"./profile/{task_name}",
        files = TradetronTaskConfigFiles(credentials = f"./profile/{task_name}/credentials.json.secret")
    )
    return task_config

def save_task_config(task_config: TradetronTaskConfig) -> None:
    # create profile path
    subprocess.run(['mkdir', '--parents', task_config['profile_path']])
    
    # add task profile
    app_config.tasks[task_config['name']] = task_config
    app_utils.write_config(
        file_path = f"{app_config.paths['profile']}/actions.yaml", 
        config = app_config.tasks
    )
    return

def save_credentials(credentials: Credentials, file_path: str) -> None:
    write_encrypted_config.main(config = dict(**credentials), file_path = file_path)
    return

def setup_schedule(task_config: TradetronTaskConfig) -> None:
    systemd_units_store_path: str = app_config.services['tradetron']['systemd']['path']
    service_template_file: str = app_config.services['tradetron']['systemd']['sub_service_login']['service']
    timer_template_file: str = app_config.services['tradetron']['systemd']['sub_service_login']['timer']

    # edit said service and timer files
    service_index: int = service_template_file.find('.service')
    service_file: str = service_template_file[:service_index] + task_config['name'] + service_template_file[service_index:]

    timer_index: int = timer_template_file.find('.timer')
    timer_file: str = timer_template_file[:timer_index] + task_config['name'] + timer_template_file[timer_index:]

    systemd_config: Dict[Any, Any] = app_utils.read_config(file_path = f"{app_config.paths['app_config']}/systemd.yaml")

    # copy service and timer files to appropriate location
    subprocess.run(
        [
            'cp', 
            f"{systemd_units_store_path}/{service_template_file}",
            f"{systemd_config['unit_install_path']}/{service_file}"
        ]
    )
    subprocess.run(
        [
            'cp', 
            f"{systemd_units_store_path}/{timer_template_file}",
            f"{systemd_config['unit_install_path']}/{timer_file}"
        ]
    )
    
    # run systemctl commands
    return

def main(task_name: str, credentials: Credentials) -> None:
    task_config: TradetronTaskConfig = create_task_config(task_name = task_name)
    save_task_config(task_config = task_config)
    save_credentials(credentials = credentials, file_path = task_config['files']['credentials'])
    setup_schedule(task_config = task_config)
    return
    setup_schedule()
    return
