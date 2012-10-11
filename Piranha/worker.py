import Corellia
from time import sleep

class BaseWorker(object):
	result_ttl = None

	def run(self, queuepool_addr, queue):
		while True:
			try:
				self.queue = Corellia.Client(queuepool_addr)
				while True:
					key, msg = self.queue.pop_task(queue)
					res = self.handle(msg)
					if res != None:
						self.queue.put_result(queue, key, res, self.result_ttl)
					self.queue.finish_task(queue, key)
			except KeyboardInterrupt:
				return
			except Exception:
				sleep(1)
				continue

class MultiTaskWorker(BaseWorker):
	def handle(self, msg):
		func, args = msg
		return getattr(self, func, lambda *args: None)(*args)

