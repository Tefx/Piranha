import Corellia

class Client(object):
    def __init__(self, queue_addr, queue):
        self.client = Corellia.Client(queue_addr)
        self.queue_addr = queue_addr
        self.queue = queue

    def add_mod(self, name, mod, num):
        for _ in xrange(num):
            self.client.push_task(self.queue, ("register", (name, mod)))

    def del_mod(self, name, num):
        for _ in xrange(num):
            self.client.push_task(self.queue, ("unregister", (name,)))

    def handle(self, *args):
        key = self.client.push_task(self.queue, args)
        return Result(self.queue_addr, self.queue, key)

    def __getattr__(self, func):
        def call(*args):
            key = self.client.push_task(self.queue, (func, args))
            return Result(self.queue_addr, self.queue, key)
        return call

class Result(object):
    def __init__(self, queue_addr, queue, key):
        self.key = key
        self.queue = queue
        self.queue_addr = queue_addr

    def status(self):
        client = Corellia.Client(self.queue_addr)
        self.value = client.get_result(self.queue, self.key)
        return self.value != None

if __name__ == '__main__':
    c = Client(("localhost", 9999), "common")