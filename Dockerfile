FROM python:3.5-slim

EXPOSE 8000


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY config.sh /usr/src/app/
RUN bash config.sh
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD python server.py
