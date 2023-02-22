#!/bin/bash

$APP_DIR = ~/apps/scheduled_login_tradetron/
cd $APP_DIR

python3 -m venv env
source env/bin/activate

python3 -m pip install -r ./setup/requirements.txt