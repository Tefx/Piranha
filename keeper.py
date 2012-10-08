import sys
sys.path.append("/Users/zzm/Desktop/Corellia")

import Corellia

from gevent.queue import Queue

class Keeper(object):
	def __init__(self):
		self.waitting_queue = Queue()

	def put(self, key, task):
		self.waitting_queue.put((key, task))
		return 'ok'

	def get(self):
		return self.waitting_queue.get()

	def state(self):
		return str(self.waitting_queue)

if __name__ == '__main__':
	Corellia.Worker(Keeper).run_alone(9999)
