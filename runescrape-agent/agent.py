import logging
import os
import sys

import requests

from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(stream=sys.stdout, level=os.environ.get(
    "LOG_LEVEL", 20), format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
sched = BlockingScheduler()
logging.info("Scheduler started")


@sched.scheduled_job('cron', minute='*/5')
def push_prices():

    # Grab prices
    raw_prices = requests.get(
        "https://storage.googleapis.com/osb-exchange/summary.json")
    logging.debug(raw_prices.text)

    items = list(raw_prices.json().values())

    # Post list to server
    try:
        r = requests.post("http://{host}:{port}/{endpoint}".format(host=os.environ.get(
            "RUNESCRAPE_SERVICE", "httpbin.org"), endpoint=os.environ.get(
                "RUNESCRAPE_ENDPOINT", "/post"), port=os.environ.get(
                    "RUNESCRAPE_PORT", "80")), json=items)

        logging.info(r.text)
        logging.info(r.headers.get("Server-Timing", "Couldn't get server timing"))
    except requests.exceptions.ConnectionError:
        logging.error("connection error")
        pass


sched.start()
