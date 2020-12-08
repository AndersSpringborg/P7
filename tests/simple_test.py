import pytest
import test
import requests
import subprocess as proc
import threading
import time


def start_services():
    api = threading.Thread(target = proc.run, args = (['python3', '../API/api.py', 'local'],))
    db = threading.Thread(target = proc.run, args = (['python3', '../database/apiDB.py'],))
    recommender = threading.Thread(target = proc.run, args = (['python3', '../recommender/webapp.py'],))
    api.start()
    db.start()
    recommender.start()
    time.sleep(3)


def test_components():
    start_services()

    requests.post('http://127.0.0.1:49500/global_prices', headers = test.headers, json = test.global_prices)
    requests.post('http://127.0.0.1:49500/data/transactions', headers = test.headers, data = test.transactions)
    requests.post('http://127.0.0.1:49500/data/wine_deals', headers = test.headers, json = test.offers)
    response = requests.post('http://127.0.0.1:49500/data/time', headers = test.headers, json = test.time_interval)
    requests.post('http://127.0.0.1:49500/data/wine_deals', headers = test.headers, json = test.offers)

    test.test_get_recommendation()
    test.test_get_wine()
