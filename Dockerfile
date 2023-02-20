FROM selenium/standalone-chrome:latest

ENV APP_HOME /usr/src/scheduled_login_tradetron
WORKDIR /$APP_HOME

COPY . $APP_HOME/

RUN pip install -r requirements.txt

CMD python app