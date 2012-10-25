from Husky import loads, dumps
import struct
from hashlib import sha224
from gevent import sleep

mods = ["test"]

def test(bytes):
    print sha224(bytes).hexdigest()
    return dumps(loads(bytes))

if __name__ == '__main__':
    import sys; sys.path.append("../")
    from Piranha import Client, config
    # c = Client(config.rootproject_addr, "/")
    b = dumps(lambda x: x)
    print repr(b)
    print len(b)
    # print sha224(b).hexdigest()
    # r = c.test_mod.test(b)
    # # print loads(b)

    # # l = loads(dumps(loads))
    # # print l
    # # print l(b)
    # sleep(1)
    # print r.status()
    # print r.value