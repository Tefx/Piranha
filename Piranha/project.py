from queue import TaskQueue
from Thinkpol import Telescreen
import config
from task import RemoveWorkerTask, NewWorkerTask

class Project(Telescreen):
    monitoring = ["path"]

    def __init__(self, path, db_conf, root=False):
        super(Project, self).__init__()
        self._connect(config.miniture_addr)
        self.path = path
        self.db_conf = db_conf
        if root:
            self.children = {"*": TaskQueue(self.join_path("*"), self.db_conf)}
        else:
            self.children = {}

    def join_path(self, name):
        return self.path + "/" + name

    def split_path(self, path):
        r = path.strip("/").partition("/")
        return r[0], r[2]

    def add_task(self, path, *args):
        return self.add_child(path, True, *args)

    def add_project(self, path):
        return self.add_child(path)

    def add_child(self, path, task=False, *args):
        name, path = self.split_path(path)
        if path:
            child = self.children.get(name, None)
            if not child: return False
            return child.add_child(path, task, *args)
        else:
            if task:
                self.children[name] = TaskQueue(self.join_path(name), self.db_conf, *args)
            else:
                self.children[name] = Project(self.join_path(name), self.db_conf)
            return True

    def delete_child(self, path):
        name, path = self.split_path(path)
        child = self.children.get(name, None)
        if not child: return False
        if path:
            return child.delete_child(path)
        else:
            child._close_connection()
            del self.children[name]
            return True

    def find_handler(self, path):
        name, path = self.split_path(path)
        child = self.children.get(name, None)
        if not child:
            return None
        if path:
            return child.find_handler(path)
        else:
            return child.handler

    def add_workers(self, path, num):
        for _ in xrange(num):
            self.children["*"].push_task(NewWorkerTask(self.find_handler(path), path))

    def delete_workers(self, path, num):
        name, path = self.split_path(path)
        child = self.children.get(name, None)
        if not child:
            return None
        if path:
            return child.delete_workers(path, num)
        else:
            for _ in xrange(num):
                child.push_task(RemoveWorkerTask())
            return True

    def __getattr__(self, func):
        if func == "child_names":
            return {k:v._uuid for k,v in self.children.iteritems()}

        def f(path, *args):
            child_name, path = self.split_path(path)
            child = self.children.get(child_name, None)
            if child:
                function = getattr(child, func, lambda *args: None)
            if isinstance(child, TaskQueue):
                return function(*args)
            elif isinstance(child, Project):
                return function(path, *args)
        return f
