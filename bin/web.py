#!/usr/bin/env python
 
import sys;sys.path.append("../")
from Piranha import config, Task
from bottle import get, post, request, response, run
import Corellia
import json

@post("/<path:path>")
def push_task(path):
    key = Corellia.call(config.queuepool_addr, "push_task", (path, Task(request.json)))
    response.set_header("key", key)

@put("/<path>/<key>")
def push_task(path, key):
    res = Corellia.call(config.queuepool_addr, "fetch_result", (path, key))
    return json.dumps(res)

if __name__ == '__main__':
    run(server=config.web_server, port=config.web_port)