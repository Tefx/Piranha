from Piranha import config
from bottle import get, put, request, response, run
import Corellia

queuepool_addr = (config.queuepool_host, config.queuepool_port)
client = Corellia.Client(queuepool_addr)
import json

@get("/result/<taskorproject>/<key>")
def get_result(taskorproject, key):
    response.content_type = "application/json"
    data = Corellia.call(queuepool_addr, "get_result", (taskorproject, key))
    return json.dumps(data)

@put("/task/<task>")
def push_task(task):
    key = Corellia.call(queuepool_addr, "push_task", (task, request.json))
    response.set_header("key", key)

@put("/task/<project>/<task>")
def push_task(project, task):
    key = Corellia.call(queuepool_addr, "push_task", (project, (task, request.json)))
    response.set_header("key", key)

if __name__ == '__main__':
    run(server=config.web_server, port=config.web_port)