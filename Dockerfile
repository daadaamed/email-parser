FROM python:3.9-slim

WORKDIR /usr/src/app

RUN pip install pytest lxml beautifulsoup4
