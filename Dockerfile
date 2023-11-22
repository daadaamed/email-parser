FROM python:3.9-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y 

RUN pip install pytest lxml beautifulsoup4
