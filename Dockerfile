FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD  f1_telemetry/ /app

CMD [ "python", "async.py"]
