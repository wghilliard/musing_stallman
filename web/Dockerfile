FROM alpine:latest

RUN apk update && apk add python3 curl

RUN cd /tmp && curl -Ok https://bootstrap.pypa.io/get-pip.py && python3 ./get-pip.py

COPY . /opt/musing_stallman

RUN cd /opt/musing_stallman && pip3 install --no-cache -r ./requirements.txt

ENTRYPOINT python3 /opt/musing_stallman/runserver.py
