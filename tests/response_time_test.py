import pytest
import test
import simple_test as st
import requests
import subprocess as proc
import threading
import time

# TODO: Add a lot more content than what's defined in 'test' module.
# Loads database component with content.
def load_db():
    st.start_services()
    requests.post('http://127.0.0.1:49500/global_prices', headers = test.headers, json = test.global_prices)
    requests.post('http://127.0.0.1:49500/data/wine_deals', headers = test.headers, json = test.offers)
    requests.post('http://127.0.0.1:49500/data/transactions', headers = test.headers, data = test.transactions)
    requests.post('http://127.0.0.1:49500/data/time', headers = test.headers, json = test.time_interval)
    requests.post('http://127.0.0.1:49500/data/wine_deals', headers = test.headers, json = test.offers)

# Creates 'expr_count' number of client instances that execute lambda expression concurrently.
def exec_expr_conc(expr_count, expr):
    threads = list()

    for i in range(1, expr_count):
        threads.append(threading.Thread(target = expr))

    start = time.time()

    for thr in threads:
        thr.start()

    for thr in threads:
        thr.join()

    return time.time() - start

# Test worst-case response time for reading a single wine.
def test_read_wine_respone_time():
    worst = 0
    pids = st.start_services()
    
    for i in range(1000):
        time = exec_expr_conc(10, lambda: test.test_get_wine())

        if (time > worst):
            worst = time
    
    st.stop_services(pids)
    print("Worst-case response time (1000 cycles): " + str(worst) + " seconds.")
    
    assert worst <= 1

# Test worst-case response time for reading recommendation.
def test_read_recommendation_response_time():
    worst = 0
    pids = st.start_services()

    for i in range(1000):
        time = exec_expr_conc(10, lambda: test.test_get_recommendation())

        if (time > worst):
            worst = time
    
    st.stop_services(pids)
    print("Worst-case response time (1000 cycles): " + str(worst) + " seconds.")

    assert worst <= 1