import requests
import json
from gevent import sleep

def test_http():
    baseurl = "http://localhost:8080/"
    r = requests.post(baseurl+"test/add", data=json.dumps((1,2)), headers={'content-type': 'application/json'})
    result_url = baseurl + "test/add/" + r.headers["key"]
    print result_url
    while True:
        r = requests.get(result_url)
        if r.json:
            print r.json
            break
        sleep(0.2)

if __name__ == '__main__':
    test_http()