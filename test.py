import sys
sys.path.append("/Users/zzm/Desktop/Corellia")

import Corellia
from gevent import sleep
from gevent.pool import Pool

def test_single(no):
	k = Corellia.Client(("localhost", 9999))
	key = k.push_task(no)
	res = None
	while res == None:
		try:
			res = k.get_result(key)
		except Exception:
			try:
				k = Corellia.Client(("localhost", 9999))
				res = k.get_result(key)
			except Exception:
				pass
		sleep(0.2)
	print key, no, res

def test_2():
	k = Corellia.Client(("localhost", 9999))
	print k.push_task(123)
	print k.push_task(223)
	print k.status()
	key, item =  k.pop_task()
	print key, item
	print k.status()
	sleep(6)
	print k.status()
	print k.put_result(key, 10)
	print k.status()
	sleep(6)
	print k.status()

if __name__ == '__main__':
	pool = Pool(1000)
	pool.map(test_single, xrange(10))
	#test_single(1)

	# test_2()

 