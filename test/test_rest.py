import sys; sys.path.append("../")
import config
import requests
import json
from gevent import sleep
import Husky

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

def test_uce_reg(name, f):
    baseurl = "http://localhost:8080/uce/"
    r = requests.post(baseurl+"reg_mod", data=json.dumps((name, Husky.dumps(f))), headers={'content-type': 'application/json'})
    print r.headers

def test_uce_eval(g):
    baseurl = "http://localhost:8080/uce/"
    r = requests.post(baseurl+"eval", data=json.dumps((g,)), headers={'content-type': 'application/json'})
    result_url = baseurl + "eval/" + r.headers["key"]
    print result_url
    while True:
        r = requests.get(result_url)
        if r.json:
            print r.json
            break
        sleep(0.2)

if __name__ == '__main__':

    g = {
        "a" : 3,
        "b" : [1, 2, 3, 4],
        "x": ["!", "double", "a"],
        "_y": ["!", "add", "x", "#b"]
    }

    # def add(x, y):
    #     return x+y

    # def double(x):
    #     return x*2

    # test_uce_reg("add", add)
    # test_uce_reg("double", double)

    test_uce_eval(g)

