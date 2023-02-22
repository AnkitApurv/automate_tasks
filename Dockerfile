FROM selenium/standalone-chrome:latest
FROM python:latest

ENV ${APP_HOME} = /opt/scheduled_login_tradetron

RUN mkdir -P ${APP_HOME}

WORKDIR ${APP_HOME}

COPY . .

RUN pip install -r ./setup/requirements.txt