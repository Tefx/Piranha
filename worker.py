import sys
sys.path.append("/Users/zzm/Desktop/Corellia")

import Corellia

class Worker(object):
	def run(self, keeper_addr, store_addr):
		self.keeper = Corellia.Client(keeper_addr)
		self.store = Corellia.Client(store_addr)
		while True:
			key, msg = self.keeper.get()
			self.store.put(key, self.handle(msg))

	def handle(self):
		pass

if __name__ == '__main__':
	from time import sleep
	class EchoWorker(Worker):
		def handle(self, msg):
			sleep(0.1)
			print msg
			return msg
	EchoWorker().run(("localhost", 9999), ("localhost", 9998))
