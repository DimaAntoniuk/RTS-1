FROM python:3.7

WORKDIR /home/script

ENV DOCKER_HOST tcp://localhost
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY mosquitto mosquitto

COPY yr903parser.py checkpointId.txt ./

CMD ["python", "./yr903parser.py"]
