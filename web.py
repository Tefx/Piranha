import sys
sys.path.append("/Users/zzm/Desktop/Corellia")

from bottle import get, put, request, response, run
import Corellia 

queuepool_addr = ("localhost", 9999)
client = Corellia.Client(queuepool_addr)
import json

@get("/<task>/<key>")
def get_result(task, key):
    response.content_type = "application/json"
    data = Corellia.call(queuepool_addr, "get_result", (task, key))
    return json.dumps(data)

@put("/<task>")
def push_task(task):
    key = Corellia.call(queuepool_addr, "push_task", (task, request.json))
    response.set_header("key", key)

if __name__ == '__main__':
    run(server='auto', port=8080)