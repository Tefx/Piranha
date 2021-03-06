import sys;sys.path.append("../")
from Piranha import config
from Thinkpol import Agent
import Corellia


def add_mod(name, mod, num):
    k = Corellia.Client(("localhost", 9999))
    for _ in xrange(num):
        key = k.push_task("common", ("register", (name, mod)))

def del_mod(name, num):
    k = Corellia.Client(("localhost", 9999))
    for _ in xrange(num):
        key = k.push_task("common", ("unregister", (name,)))


if __name__ == '__main__':
    def add(x, y):
        return x+y

    add_mod("add", add, 3)
    # del_mod("add", 2)
    miniture_host, miniture_port = config.miniture_addr
    miniture_port += 1
    Smith = Agent((miniture_host, miniture_port))

    print Smith.fetch()

