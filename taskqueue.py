from uuid import uuid4
gen_key = lambda : uuid4().hex

from gevent import sleep
from time import time
import gevent

class TaskQueue(object):
	def __init__(self, name, C_queue, C_kvstore, C_set, timeout=5):
		self.name = name
		self.waitting_queue = C_queue(self.make_name("waitting_queue"))
		self.running_queue = C_queue(self.make_name("running_queue"))
		self.result_store = C_kvstore(self.make_name("result_store"))
		self.finished_task = C_set(self.make_name("finished_task"))
		gevent.spawn(self.cheanup_let, timeout)

	def make_name(self, name):
		return "%s_%s" % (self.name, name)

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

	def finish_task(self, key):
		self.finished_task.add(key)

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
			if k not in self.finished_task:
				if hasattr(self.waitting_queue, "lpush"):
					self.waitting_queue.lpush(item)
				else:
					self.waitting_queue.push(item)
			else:
				self.finished_task.remove(k)


if __name__ == '__main__':
	import sys
	sys.path.append("/Users/zzm/Desktop/Corellia")
	import Corellia
	import structs
	Corellia.Worker(TaskQueue, structs.RedisQueue, structs.RedisKVStore, sturcts.BuiltinSet).run_alone(9999)
