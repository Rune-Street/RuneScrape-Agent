import schedule
import requests
import time
import os
import logging
import sys


def push_prices():

    # Grab prices
    raw_prices = requests.get(
        "https://storage.googleapis.com/osb-exchange/summary.json")
    logging.debug(raw_prices.text)

    items = list(raw_prices.json().values())

    # Post list to server
    try:
        r = requests.post("http://{}/items".format(os.environ.get(
            "RUNESCRAPE_SERVICE", "httpbin.org/post")), json=items)
        logging.info(r.text)
    except requests.exceptions.ConnectionError:
        logging.error("connection error")
        pass


logging.basicConfig(stream=sys.stdout, level=os.environ.get("LOG_LEVEL", 20))
schedule.every(5).minutes.do(push_prices)
print(os.environ.get("RUNESCRAPE_SERVICE"))
while True:
    schedule.run_pending()
    time.sleep(5)


push_prices()
