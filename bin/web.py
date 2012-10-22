#!/usr/bin/env python
 
import sys;sys.path.append("../")
from Piranha import config, Task
from bottle import get, post, request, response, run
import Corellia
import json


@get("/")
def hello():
    return "hello world"

@post("/<path:path>")
def push_task(path):
    key = Corellia.call(config.queuepool_addr, "push_task", (path, Task(request.json)))
    response.set_header("key", key)

@get("/<path:path>")
def get_result(path):
    path,_,key = path.strip("/").rpartition("/")
    response.content_type = "application/json"
    res = Corellia.call(config.queuepool_addr, "fetch_result", (path, key))
    return json.dumps(res)

if __name__ == '__main__':
    run(server=config.web_server, port=config.web_port, host='0.0.0.0')