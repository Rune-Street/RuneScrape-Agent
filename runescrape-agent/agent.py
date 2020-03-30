import schedule
import requests
import time
import os
import logging
import sys


def push_prices():

    # Grab prices
    item_prices = requests.get(
        "https://storage.googleapis.com/osb-exchange/summary.json")
    logging.info(item_prices.text)

    # Post list to server
    try:
        requests.post("http://{}/items".format(os.environ.get("RUNESCRAPE_SERVICE", "httpbin.org/post")), json=item_prices.text)
        # r = requests.post("http://{}/items".format(os.environ["RUNESCRAPE_SERVICE"]),
        #                   json=json.dumps(item_price_json))
    except requests.exceptions.ConnectionError:
        print("connection error")
        pass


logging.basicConfig(stream=sys.stdout, level=os.environ.get("LOG_LEVEL", 20))
schedule.every(5).minutes.do(push_prices)
while True:
    schedule.run_pending()
    time.sleep(5)
