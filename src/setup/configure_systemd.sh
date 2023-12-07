#!/bin/bash

cp -r ../systemd/ ~/.config/systemd/user/

systemctl --user start scheduled_login_tradetron_login.service
systemctl --user enable scheduled_login_tradetron_login.timer
systemctl --user start scheduled_login_tradetron_login.timer

systemctl --user start scheduled_login_tradetron_manage_creds.service