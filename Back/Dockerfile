###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.3-slim as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    python3-dev musl-dev libffi-dev\
    && pip install psycopg2

# lint
RUN pip install --upgrade pip
COPY . .

# install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

COPY . .

#########
# FINAL #
#########

# pull official base image
FROM python:3.8.3-slim

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y libpq-dev bash netcat python-pydot python-pydot-ng graphviz
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME
RUN chown -R app:app /var/log/
RUN chown -R app:app /var/run/

EXPOSE 8000

# change to the app user
USER app

CMD ["gunicorn", "Config.asgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "-k","uvicorn.workers.UvicornWorker","--log-file","-"]
