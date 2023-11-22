FROM python:3.9-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y libxml2 libxml2-dev libxslt1.1 libxslt1-dev zlib1g-dev

RUN pip install pytest lxml beautifulsoup4
