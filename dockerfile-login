FROM mcr.microsoft.com/playwright:next
FROM python:slim

ENV ${APP_HOME} = /app
ENV ${pip_reqire} = requirements-login.txt

COPY app .
COPY setup/${pip_reqire} .

RUN pip install -r ${pip_reqire}

CMD python -m app.login