import pytest
import test
import requests
import subprocess as proc
import threading
import time
import subprocess
import os

def start_services():
    api_pid = subprocess.Popen(["python3", "../API/api.py", "local"]).pid
    db_pid = subprocess.Popen(["python3", "../database/apiDB.py"]).pid
    rec_pid = subprocess.Popen(["python3", "../recommender/webapp.py"]).pid
    time.sleep(3)

    return [api_pid, db_pid, rec_pid]

def stop_services(pids):
    for pid in pids:
        os.kill(pid, 9)

def test_components():
    pids = start_services()

    requests.post('http://127.0.0.1:49500/global_prices', headers = test.headers, json = test.global_prices)
    requests.post('http://127.0.0.1:49500/data/wine_deals', headers = test.headers, json = test.offers)
    requests.post('http://127.0.0.1:49500/data/transactions', headers = test.headers, data = test.transactions)
    requests.post('http://127.0.0.1:49500/data/time', headers = test.headers, json = test.time_interval)
    requests.post('http://127.0.0.1:49500/data/wine_deals', headers = test.headers, json = test.offers)

    test.test_get_recommendation()
    test.test_get_wine()

    stop_services(pids)