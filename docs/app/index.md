# Scheduled Login : Tradetron

## Adding new automated task

1. Decide on a name for your task, use that name for new task to be added (described in sets below), Example: __task_a__
2. Follow instructions below for each of the specified app modules:
    1. profile
        1. create folder named __task_a__, place your __task_a__ related necessary files in this folder
        2. edit profile/profile.json as shown below:
        ```json
        {
            "task_a": {
                "file_alias": "file_name",
            }
        }
        ```
    2. automate_tasks
        1. create python package named __task_a__, whih will actually perform __task_a__.
    3. if __task_a__ requires secrets management, manage_task_secrets
        1. create python package named __task_a__
        2. this package will contain scripts for entire lifecycle of secret management
        3. ideally these scripts should provide interface using both _argparser_ and _pywebio_.

## How will automated task be scheduled

using systemd services and timers, optionally we can have a service for failure notification

### how will newly added tasks be incorporated into schedule

unsolved

### how will the web interface for newly added _manage_task_secrets_ package be incorporated into running web app

unsolved

## Removing an automated task

unsolved
