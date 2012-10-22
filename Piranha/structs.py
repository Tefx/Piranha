from gevent import monkey; monkey.patch_all()
from redis import StrictRedis
import sys; sys.path.append("/Users/zzm/Desktop/Husky")
import Husky

class RedisStruct(object):
	def __init__(self, name, db_conf):
		self.name = name
		self.redis = StrictRedis(host=db_conf["host"], port=db_conf["port"], db=db_conf["db"])	


class RedisQueue(RedisStruct):
	def pop(self):
		return Husky.loads(self.redis.blpop(self.name, 0)[1])

	def rpop(self):
		return Husky.loads(self.redis.brpop(self.name, 0)[1])

	def push(self, item):
		self.redis.rpush(self.name, Husky.dumps(item))
		return True

	def lpush(self, item):
		self.redis.lpush(self.name, Husky.dumps(item))
		return True


class RedisPriorityQueue(RedisStruct):
	def __init__(self, *args):
		super(RedisPriorityQueue, self).__init__(*args)
		self.helper = self.name + "helper"

	def pop(self):
		item = self.redis.zrevrange(self.name, 0, 0)
		item2 = self.redis.blpop(self.helper, 0)
		if item:
			item = item[0]
		else:
			item = item2[1]
		self.redis.zrem(self.name, item)
		return Husky.loads(item)

	def push(self, item, rank=0):
		self.redis.zadd(self.name, rank, Husky.dumps(item))
		self.redis.lpush(self.helper, Husky.dumps(item))
		return True


class RedisKVStore(RedisStruct):
	def put(self, key, value, ttl=None):
		value = Husky.dumps(value)
		if ttl:
			self.redis.setex("%s_%s" % (self.name, key), ttl, value)
		else:
			self.redis.set("%s_%s" % (self.name, key), value)
		return key

	def get(self, key):
		res = self.redis.get("%s_%s" % (self.name, key))
		if res:
			return Husky.loads(res)
		else:
			return False	


class RedisSet(RedisStruct):
	def add(self, value):
		self.redis.sadd(self.name, value)

	def remove(self, value):
		self.redis.srem(self.name, value)

	def __contains__(self, value):
		return self.redis.sismember(self.name, value)


class RedisHashes(RedisStruct):
	def set(self, name, value):
		self.redis.hset(self.name, name, value)
		return True

	def remove(self, name):
		self.redis.hdel(self.name, name)
		return True

	def getall(self):
		return self.redis.hgetall(self.name)

if __name__ == '__main__':
	pq = RedisPriorityQueue("test", {
									"host" : "localhost",
									"port" : 6379,
									"db" : 0
									})

	pq.push(1, 1)
	pq.push(2, 0)
	pq.push(3, 3)

	print "pushed"

	print pq.pop()
	print pq.pop()
	print pq.pop()
	print pq.pop()
