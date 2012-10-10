from taskqueue import TaskQueue


class QueuePool(object):
	def __init__(self, queues):
		self.queues = {name:TaskQueue(name, *args) for name,args in queues.iteritems()}

	def __getattr__(self, func):
		return lambda queue, *args: \
				getattr(self.queues[queue], func, lambda *args: None)(*args)


if __name__ == '__main__':
	import sys
	sys.path.append("/Users/zzm/Desktop/Corellia")
	import Corellia
	from structs import RedisQueue, RedisKVStore, RedisSet
	Corellia.Worker(QueuePool, {"echo":(RedisQueue, RedisKVStore, RedisSet)}).run_alone(9999)