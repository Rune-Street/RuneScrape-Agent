from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import os
import logging
import sys


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
        r = requests.post("http://{host}/{endpoint}".format(host=os.environ.get(
            "RUNESCRAPE_SERVICE", "httpbin.org"), endpoint=os.environ.get(
                "RUNESCRAPE_ENDPOINT", "/post")), json=items)

        logging.info(r.text)
    except requests.exceptions.ConnectionError:
        logging.error("connection error")
        pass


sched.start()
