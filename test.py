import sys
sys.path.append("/Users/zzm/Desktop/Corellia")

import Corellia
from uuid import uuid4
from gevent import sleep
from gevent.pool import Pool

def test_single(no):
	k = Corellia.Client(("localhost", 9999))
	s = Corellia.Client(("localhost", 9998))
	key = uuid4().int
	value = key % 100
	k.put(key, value)
	res = None
	while not res:
		res = s.get(key)
		sleep()
	print no, key, res

if __name__ == '__main__':
	pool = Pool(1000)
	pool.map(test_single, xrange(20))

	