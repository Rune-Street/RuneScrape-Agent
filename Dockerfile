FROM python:3.8.2-alpine3.11

RUN adduser -D -g '' runescrape
WORKDIR /home/runescrape
USER runescrape

COPY requirements.txt /tmp
RUN pip3 install --no-warn-script-location -r /tmp/requirements.txt

COPY runescrape-agent .

CMD python3 runescrape-agent/agent.py
