FROM python:3.9

WORKDIR /Xana
COPY . /Xana

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y cron

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /Xana/requirements.txt

WORKDIR /Xana

# running migrations
RUN python manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

