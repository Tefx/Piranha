import Corellia


class Client(object):
    def __init__(self, root_addr, path):
        self.client = Corellia.Client(root_addr)
        self.root_addr = root_addr
        if path == "/": path = ""
        self.path = path

    def join_path(self, name):
        if self.path == "":
            return name
        else:
            return self.path + "/" + name

    def add_project(self, name):
        return self.client.add_project(self.join_path(name))

    def add_task(self, name, func):
        return self.client.add_task(self.join_path(name, func))

    def add_workers(self, num):
        return self.client.add_workers(self.path, num)

    def delete_workers(self, num):
        return self.client.delete_workers(self.path, num)

    def delete(self, name):
        self.client.delete(self.join_path(name))

    def __getattr__(self, name):
        return Client(self, root_addr, self.path.join_path(name))

    def __call__(self, *args):
        key = self.client.push_task(self.path, Task(args))

    def push_task(self, args):
        return self.client.push_task(self.path, Task(args))

    def fetch_result(self, key):
        return self.client.fetch_result(self.path, key)


class Result(object):
    def __init__(self, root_addr, path, key):
        self.key = key
        self.path = path
        self.root_addr = root_addr

    def status(self):
        client = Corellia.Client(self.root_addr)
        self.value = client.fetch_result(self.path, self.key)
        return self.value != None