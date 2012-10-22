import Corellia
import task as tasktypes
from gevent import sleep
from Thinkpol import Telescreen
import config


class Worker(Telescreen):
	monitoring = ["path", "func"]

	def __init__(self, root_addr):
		super(Worker, self).__init__()
		self.root_addr = root_addr
		self.path = "*"
		self.func = None
		self._connect(config.miniture_addr)

	def run(self):
		self.queue = None
		while True:
			if not self.queue:
				try:
					self.queue = Corellia.Client(self.root_addr)
				except KeyboardInterrupt:
					break
				except Exception:
					sleep(2)
					continue
			task = self.queue.pop_task(self.path)
			if not task:
				self.queue = None
				continue
			try:
				res = self.handle(task)
				self.queue.finish_task(self.oldpath, task.key)
			except KeyboardInterrupt:
				break
			except Exception:
				continue
			if res != None:
				if not self.queue.register_result(self.path, task.key, res):
					self.queue = None
					continue

	def handle(self, task):
		self.oldpath = self.path
		if isinstance(task, tasktypes.NewWorkerTask):
			self.path = task.path
			self.func = task.get_body()
		elif isinstance(task, tasktypes.RemoveWorkerTask):
			self.path = "*"
		else:
			return self.func(*(task.get_body()))


