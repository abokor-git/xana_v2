FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip

RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y cron

WORKDIR /home/
RUN git clone https://github.com/abokor-git/xana_v2
WORKDIR /home/xana_v2/

RUN pip install --no-cache-dir -r /home/xana_v2/requirements.txt