from time import time
from uuid import uuid4
gen_key = lambda : uuid4().hex
import Husky

class Task(object):
    def __init__(self, body, priority=0):
        super(Task, self).__init__()
        self.body = Husky.dumps(body)
        self.priority = priority
        self.create_time = time()

    def set_queue_time(self):
        self.queue_time = time()

    def set_handle_time(self):
        self.handle_time = time()

    def set_key(self):
        self.key = gen_key()
        return self.key

    def get_body(self):
        return Husky.loads(self.body)

class RemoveWorkerTask(Task):
    def __init__(self):
        super(RemoveWorkerTask, self).__init__(None, 1)

class NewWorkerTask(Task):
    def __init__(self, func, path):
        super(NewWorkerTask, self).__init__(func, 1)
        self.path =path

