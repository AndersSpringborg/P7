import test
import requests

def test_components():
    requests.post('http://127.0.0.1:49500/global_prices', headers = test.headers, json = test.global_prices)
    requests.post('http://127.0.0.1:49500/data/transactions', headers = test.headers, data = test.transactions)
    requests.post('http://127.0.0.1:49500/data/wine_deals', headers = test.headers, json = test.offers)
    response = requests.post('http://127.0.0.1:49500/data/time', headers = test.headers, json = test.time_interval)
    requests.post('http://127.0.0.1:49500/data/wine_deals', headers = test.headers, json = test.offers)

    test.test_get_recommendation()
    test.test_get_wine()

test_components()