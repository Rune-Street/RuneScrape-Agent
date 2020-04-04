FROM python:3.8.2-alpine3.11

RUN adduser -D -g '' runescrape
WORKDIR /home/runescrape
USER runescrape

ENV PATH="/home/runescrape/.local/bin:${PATH}"
COPY --chown=runescrape:runescrape requirements.txt /tmp
RUN pip3 install --user -r /tmp/requirements.txt

COPY --chown=runescrape:runescrape runescrape-agent runescrape-agent

CMD python3 runescrape-agent/agent.py
