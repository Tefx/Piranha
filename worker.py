import sys
sys.path.append("/Users/zzm/Desktop/Corellia")

import Corellia
from time import sleep

class Worker(object):
	def run(self, queue_addr):
		while True:
			try:
				self.queue = Corellia.Client(queue_addr)
			except KeyboardInterrupt:
				break
			except Exception:
				sleep(2)
				continue
			while True:
				try:
					key, msg = self.queue.pop_task()
					self.queue.put_result(key, self.handle(msg))
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
	EchoWorker().run(("localhost", 9999))
