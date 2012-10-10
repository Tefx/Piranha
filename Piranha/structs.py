from gevent import monkey
monkey.patch_all()

from gevent.queue import Queue


class GeventQueue(Queue):
	def pop(self):
		return self.get()

	def push(self, item):
		self.put(item)
		return True


class BuiltinKVStore(dict):
	def __init__(self, name, *args):
		super(BuiltinSet, self).__init__(*args)
		self.name = name	

	def put(self, key, value):
		self[key] = value
		return key

	def get(self, key):
		return self.get(key, None)

class BuiltinSet(set):
	def __init__(self, name, *args):
		super(BuiltinSet, self).__init__(*args)
		self.name = name		


from redis import StrictRedis
import json as json


class RedisStruct(object):
	def __init__(self, name):
		self.name = name
		self.redis = StrictRedis(host='localhost', port=6379, db=0)	


class RedisQueue(RedisStruct):
	def pop(self):
		return json.loads(self.redis.blpop(self.name, 0)[1])

	def rpop(self):
		return json.loads(self.redis.brpop(self.name, 0)[1])

	def push(self, item):
		self.redis.rpush(self.name, json.dumps(item))
		return True

	def lpush(self, item):
		self.redis.lpush(self.name, json.dumps(item))
		return True


class RedisKVStore(RedisStruct):
	def put(self, key, value):
		try:
			self.redis.hset(self.name, key, value)
			return key
		except Exception:
			return False

	def get(self, key):
		return self.redis.hget(self.name, key)


class RedisSet(RedisStruct):
	def add(self, value):
		self.redis.sadd(self.name, value)

	def remove(self, value):
		self.redis.srem(self.name, value)

	def __contains__(self, value):
		return self.redis.sismember(self.name, value)

if __name__ == '__main__':
	r = RedisKVStore("test")
	k = r.put(1,2)
	print r.get(k)
	print r.get(3)
	print r.exists(2)
	print r.exists(k)
