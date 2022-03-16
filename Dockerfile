FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip

RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y cron

WORKDIR /home/xana_v2/
COPY . /home/xana_v2/

RUN pip install --no-cache-dir -r /home/xana_v2/requirements.txt