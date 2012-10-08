import sys
sys.path.append("/Users/zzm/Desktop/Corellia")

import Corellia

class Store(object):
	def __init__(self):
		self.dict = {}

	def put(self, key, value):
		self.dict[key] = value
		return "ok"

	def get(self, key):
		return self.dict.get(key, None)

	def state(self):
		return self.dict

if __name__ == '__main__':
	Corellia.Worker(Store).run_alone(9998)
