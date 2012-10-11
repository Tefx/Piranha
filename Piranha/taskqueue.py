from uuid import uuid4
gen_key = lambda : uuid4().hex

from gevent import sleep
from time import time
import gevent

from structs import RedisQueue as C_queue
from structs import RedisKVStore as C_kvstore
from structs import RedisSet as C_set

class TaskQueue(object):
	def __init__(self, name, db_conf=None, timeout=5):
		self.name = name
		self.waitting_queue = C_queue(self.make_name("waitting_queue"), db_conf)
		self.running_queue = C_queue(self.make_name("running_queue"), db_conf)
		self.result_store = C_kvstore(self.make_name("result"), db_conf)
		self.finished_task = C_set(self.make_name("finished_task"), db_conf)
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

	def put_result(self, key, result, ttl=None):
		return self.result_store.put(key, result, ttl)

	def get_result(self, key):
		return self.result_store.get(key)

	def finish_task(self, key):
		self.finished_task.add(key)

	def cheanup_let(self, timeout):
		while True:
			start_time, item = self.running_queue.rpop()
			delta = time()-start_time
			if delta < timeout:
				sleep(timeout-delta)
			k,_ = item
			if k not in self.finished_task:
				self.waitting_queue.lpush(item)
			else:
				self.finished_task.remove(k)
