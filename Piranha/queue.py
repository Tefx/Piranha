from gevent import sleep
from time import time
import gevent

from structs import RedisPriorityQueue
from structs import RedisQueue
from structs import RedisKVStore
from structs import RedisSet

from Thinkpol import Telescreen
import config

class TaskQueue(Telescreen):
    monitoring = ["path", "handler"]

    def __init__(self, path, db_conf, handler=None, ttl=None, queue_timeout=60, task_timeout=5):
        super(TaskQueue, self).__init__()
        self.path = path
        self.handler = handler
        self.ttl = ttl
        self.queue_timeout = queue_timeout
        self.task_timeout = task_timeout
        self.waitting_queue = RedisPriorityQueue(self.make_name("waitting_queue"), db_conf)
        self.running_queue = RedisQueue(self.make_name("running_queue"), db_conf)
        self.result_store = RedisKVStore(self.make_name("result_dict"), db_conf)
        self.finished_task = RedisSet(self.make_name("finished_task"), db_conf)
        self._connect(config.miniture_addr)
        gevent.spawn(self.cheanup_let)

    def make_name(self, name):
        return "%s_%s" % (self.path, name)

    def push_task(self, task):
        task.set_queue_time()
        key = task.set_key()
        if self.waitting_queue.push(task, task.priority):
            return key

    def pop_task(self):
        while True:
            task = self.waitting_queue.pop()
            if time()-task.queue_time < self.queue_timeout:
                break
        task.set_handle_time()
        self.running_queue.push(task)
        return task

    def register_result(self, key, result):
        return self.result_store.put(key, result, self.ttl)

    def fetch_result(self, key):
        return self.result_store.get(key)

    def finish_task(self, key):
        self.finished_task.add(key)

    def cheanup_let(self):
        while True:
            task = self.running_queue.pop()
            delta = time()-task.handle_time
            if delta < self.task_timeout:
                sleep(self.task_timeout-delta)
            if task.key not in self.finished_task:
                self.waitting_queue.push(task, task.priority)
            else:
                self.finished_task.remove(task.key)

    def __del__(self):
        del self.waitting_queue
        del self.running_queue
        del self.result_store
        del self.finished_task 

if __name__ == '__main__':
    from task import Task
    t = TaskQueue("/A/task", {
                                "host" : "localhost",
                                "port" : 6379,
                                "db" : 0
                                })

    t.push_task(Task(1))
    print t.pop_task()
