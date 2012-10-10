from uuid import uuid4
gen_key = lambda : uuid4().hex

from gevent import sleep
from time import time
import gevent

class TaskQueue(object):
	def __init__(self, C_queue, C_kvstore, timeout=5):
		self.waitting_queue = C_queue("waitting_queue")
		self.running_queue = C_queue("running_queue")
		self.result_store = C_kvstore("result_store")
		gevent.spawn(self.cheanup_let, timeout)

	def push_task(self, task):
		key = gen_key()
		if self.waitting_queue.push((key, task)):
			return key

	def pop_task(self):
		item = self.waitting_queue.pop()
		self.running_queue.push((time(), item))
		return item

	def put_result(self, key, result):
		return self.result_store.put(key, result)

	def get_result(self, key):
		return self.result_store.get(key)

	def cheanup_let(self, timeout):
		while True:
			if hasattr(self.waitting_queue, "rpop"):
				start_time, item = self.running_queue.rpop()
			else:
				start_time, item = self.running_queue.pop()
			delta = time()-start_time
			if delta < timeout:
				sleep(timeout-delta)
			k,_ = item
			if not self.result_store.exists(k):
				if hasattr(self.waitting_queue, "lpush"):
					self.waitting_queue.lpush(item)
				else:
					self.waitting_queue.push(item)


if __name__ == '__main__':
	import sys
	sys.path.append("/Users/zzm/Desktop/Corellia")
	import Corellia
	import structs
	Corellia.Worker(TaskQueue, structs.RedisQueue, structs.RedisKVStore).run_alone(9999)
