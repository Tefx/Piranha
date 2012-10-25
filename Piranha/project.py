from queue import TaskQueue
from Thinkpol import Telescreen
import config
from task import RemoveWorkerTask, NewWorkerTask
from structs import RedisHashes

TYPE_TASKQUEUE = 1
TYPE_PROJECT = 0

class Project(object):
    def __init__(self, path, db_conf):
        super(Project, self).__init__()
        self.path = path
        self.db_conf = db_conf
        self.child_index = RedisHashes(self.make_name("child"), db_conf)
        self.children = {}
        self.rebuild()

    def join_path(self, name):
        return self.path + "/" + name

    def make_name(self, name):
        return "%s_%s" % (self.path, name)

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
            if name in self.children:
                del self.children[name]
                self.child_index.remove(name)
            if task:
                self.child_index.set(name, TYPE_TASKQUEUE)
                self.children[name] = TaskQueue(self.join_path(name), self.db_conf, *args)
            else:
                self.child_index.set(name, TYPE_PROJECT)
                self.children[name] = Project(self.join_path(name), self.db_conf)
            return True

    def delete_child(self, path):
        name, path = self.split_path(path)
        child = self.children.get(name, None)
        if not child: return False
        if path:
            child.delete_child(path)
        del self.children[name]
        self.child_index.remove(name)
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

    def rebuild(self):
        for c,v in self.child_index.getall().iteritems():
            if v == str(TYPE_TASKQUEUE):
                self.children[c] = TaskQueue(self.join_path(c), self.db_conf)
            elif v == str(TYPE_PROJECT):
                self.children[c] = Project(self.join_path(c), self.db_conf)
                self.children[c].rebuild()

    def type(self, name):
        if not name in self.children:
            return None
        elif isinstance(self.children[name], TaskQueue):
            return TYPE_TASKQUEUE
        elif isinstance(self.children[name], Project):
            return TYPE_PROJECT

    def list(self, rec=False):
        if not rec:
            return {name:self.type(name) for name in self.children.iterkeys()}
        else:
            res = {}
            for k,v in self.children.iteritems():
                if self.type(k) == TYPE_TASKQUEUE:
                    res[k] = TYPE_TASKQUEUE
                elif self.type(k) == TYPE_PROJECT:
                    res[k] = v.list()
            return res

    def __del__(self):
        for cn in self.children.iterkeys():
            self.child_index.remove(cn)
        del self.children


class RootProject(Project, Telescreen):
    monitoring = ["path", "structure"]

    def __init__(self, *args):
        super(RootProject, self).__init__("root", *args)
        self._connect(config.miniture_addr)
        self.structure = {}
        self.children["*"] = TaskQueue(self.join_path("*"), self.db_conf)
      
    def fetch_trigger(self):
        self.structure = self.list(True)
