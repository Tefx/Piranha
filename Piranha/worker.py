import Corellia
from time import sleep

class BaseWorker(object):
	def run(self, queuepool_addr, queue):
		while True:
			try:
				self.queue = Corellia.Client(queuepool_addr)
			except KeyboardInterrupt:
				break
			except Exception:
				sleep(2)
				continue
			while True:
				try:
					key, msg = self.queue.pop_task(queue)
					res, ttl = self.handle(msg)
					if res != None:
						self.queue.put_result(queue, key, res, ttl)
					self.queue.finish_task(queue, key)
				except Exception:
					break
