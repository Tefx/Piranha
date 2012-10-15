import sys; sys.path.append("../")
from time import sleep

from Piranha import Client, config

if __name__ == '__main__':
    c = Client(config.queuepool_addr, "common")
    # c.add_mod("add", lambda x,y:x+y, 2)

    # r = c.add(1, 2)
    # print r
    # print r.status()
    # sleep(1)
    # print r.status()
    # print r.value

    c.del_mod("add", 2)