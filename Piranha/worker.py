import Corellia
import task as tasktypes
from gevent import sleep
from Thinkpol import Telescreen
import config
from redis import StrictRedis
from types import FunctionType


def add_globals(func, service):
	g = func.func_globals
	g["service"] = service
	return FunctionType(func.func_code, g, func.func_closure, func.func_defaults)

class Worker(Telescreen):
	monitoring = ["path"]

	def __init__(self, root_addr):
		super(Worker, self).__init__()
		self.root_addr = root_addr
		self.path = "*"
		self.func = None
		self._connect(config.miniture_addr)
		self.set_service()

	def set_service(self):
		host = config.redis_conf["host"]
		port = config.redis_conf["port"]
		self.sevices = {
			"redis": StrictRedis(host, port, db=1),
			"modules": {
				"Husky": __import__("Husky")
			}
		}

	def run(self):
		self.queue = None
		while True:
			if not self.queue:
				try:
					self.queue = Corellia.Client(self.root_addr)
				except Exception:
					sleep(2)
					continue
			task = self.queue.pop_task(self.path)
			if not task:
				self.queue = None
				continue
			# try:
			res = self.handle(task)
			self.queue.finish_task(self.oldpath, task.key)
			# except Exception:
			# 	continue
			if res != None:
				if not self.queue.register_result(self.path, task.key, res):
					self.queue = None
					continue

	def handle(self, task):
		self.oldpath = self.path
		if isinstance(task, tasktypes.NewWorkerTask):
			self.path = task.path
			self.func = add_globals(task.get_body(), self.sevices)
		elif isinstance(task, tasktypes.RemoveWorkerTask):
			self.path = "*"
		else:
			return self.func(*(task.get_body()))


