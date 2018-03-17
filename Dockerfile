FROM python:3.6-slim

EXPOSE 8080


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN bash config.sh
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD python server.py
