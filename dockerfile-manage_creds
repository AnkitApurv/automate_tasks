FROM python:slim

ENV ${APP_HOME} = /app
ENV ${pip_reqire} = requirements-manage_creds.txt

COPY app .
COPY setup/${pip_reqire} .

RUN pip install -r ${pip_reqire}

CMD python -m app.manage_creds