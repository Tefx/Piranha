import sys
sys.path.append("/Users/zzm/Desktop/Corellia")

import Corellia
from time import sleep

class Worker(object):
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
					res = self.handle(msg)
					if res != None:
						self.queue.put_result(queue, key, res)
					self.queue.finish_task(queue, key)
				except Exception:
					break

	def handle(self):
		pass

if __name__ == '__main__':
	from time import sleep
	class EchoWorker(Worker):
		def handle(self, msg):
			print msg
			print "starting"
			sleep(1)
			print "ending"
			return msg
	EchoWorker().run(("localhost", 9999), "echo")
