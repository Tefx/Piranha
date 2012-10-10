from gevent import monkey; monkey.patch_all()
from gevent.queue import Queue

class GeventQueue(object):
	def __init__(self, name):
		self.queue = Queue()

	def pop(self):
		return self.queue.get()

	def push(self, item):
		self.queue.put(item)
		return True


class BuiltinKVStore(object):
	def __init__(self, name):
		self.store = dict()

	def put(self, key, value):
		self.store[key] = value
		return key

	def get(self, key):
		value = self.store.get(key, None)
		return value

	def exists(self, key):
		return key in self.store

from redis import StrictRedis
import json as json

class RedisQueue(object):
	def __init__(self, name):
		self.name = name
		self.redis = StrictRedis(host='localhost', port=6379, db=0)

	def pop(self):
		return json.loads(self.redis.blpop(self.name, 0)[1])

	def push(self, item):
		self.redis.rpush(self.name, json.dumps(item))
		return True


class RedisKVStore(object):
	def __init__(self, name):
		self.name = name
		self.redis = StrictRedis(host='localhost', port=6379, db=0)

	def put(self, key, value):
		try:
			self.redis.hset(self.name, key, value)
			return key
		except Exception:
			return False

	def get(self, key):
		return self.redis.hget(self.name, key)

	def exists(self, key):
		return self.redis.hexists(self.name, key)

if __name__ == '__main__':
	r = RedisKVStore("test")
	k = r.put(1,2)
	print r.get(k)
	print r.get(3)
	print r.exists(2)
	print r.exists(k)
		
		