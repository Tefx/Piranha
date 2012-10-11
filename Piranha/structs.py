from gevent import monkey; monkey.patch_all()
from redis import StrictRedis
import json as json

class RedisStruct(object):
	def __init__(self, name, db_conf):
		self.name = name
		self.redis = StrictRedis(host=db_conf["host"], port=db_conf["port"], db=db_conf["db"])	


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
	def put(self, key, value, ttl=None):
		if ttl:
			self.redis.setex("%s_%s" % (self.name, key), ttl, value)
		else:
			self.redis.set("%s_%s" % (self.name, key), value)
		return key

	def get(self, key):
		return self.redis.get("%s_%s" % (self.name, key))


class RedisSet(RedisStruct):
	def add(self, value):
		self.redis.sadd(self.name, value)

	def remove(self, value):
		self.redis.srem(self.name, value)

	def __contains__(self, value):
		return self.redis.sismember(self.name, value)
