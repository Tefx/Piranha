import Corellia
from time import sleep
from Thinkpol import Telescreen


class BaseWorker(object):
	result_ttl = None

	def run(self, queuepool_addr, queue):
		self.queue = None
		while True:
			if not self.queue:
				try:
					self.queue = Corellia.Client(queuepool_addr)
				except Exception:
					sleep(2)
					continue
			task = self.queue.pop_task(queue)
			if not task:
				self.queue = None
				continue
			key, msg = task
			try:
				res = self.handle(msg)
				self.queue.finish_task(queue, key)
			except Exception:
				continue
			if res != None:
				if not self.queue.put_result(queue, key, res, self.result_ttl):
					self.queue = None
					continue

class MultiTaskWorker(BaseWorker):	
	def handle(self, msg):
		func, args = msg
		return getattr(self, func, lambda *args: None)(*args)

class MutableWorker(MultiTaskWorker):
	def __init__(self):
		super(MutableWorker, self).__init__()
		self.mods = []

	def register(self, name, f):
		if name not in self.mods:
			setattr(self, name, f)
			self.mods.append(name)

	def unregister(self, name):
		if name in self.mods:
			delattr(self, name)
			self.mods.remove(name)

class AbstractWorker(MutableWorker, Telescreen):
    monitoring = ["mods"]

    def __init__(self, miniture_addr):
        super(AbstractWorker, self).__init__()
        self._connect(miniture_addr)

