import sys; sys.path.append("../")
from Piranha import config
from Corellia import Client
from Thinkpol import Agent
from gevent import sleep
from Piranha import Task

miniture_host, miniture_port = config.miniture_addr
miniture_port += 1
Smith = Agent((miniture_host, miniture_port))
c = Client(("localhost", config.queuepool_port))

print Smith.fetch()

def add(x, y):
    return x+y

c.add_project("test")
# c.add_project("A")
# c.add_project("A/B")
# c.add_project("C")
# sleep(1)

# print Smith.fetch()

c.add_task("test/add", add)
# sleep(1)

# print Smith.fetch()

# c.add_workers("test/add", 2)
# sleep(1)

# print Smith.fetch()

# t = c.pop_task("A/B")
# sleep(1)
# print t

# print Smith.list()
# print Smith.fetch()

# c.register_result("A/B", t.key, 10)
# sleep(1)

# print Smith.fetch()

# k = c.push_task("test/add", Task((2,4)))
# sleep(1)

# print k
# print Smith.fetch()

# print c.fetch_result("test/add", k)
# sleep(1)

# print Smith.fetch()

# c.delete_child("A/B")
# sleep(1)

# print Smith.fetch()

# c.delete_workers("A/B", 1)
# sleep(1)

# print Smith.fetch()