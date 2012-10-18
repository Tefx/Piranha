import sys;sys.path.append("../")
from Piranha import config
from Corellia import Client
from Thinkpol import Agent
from gevent import sleep

miniture_host, miniture_port = config.miniture_addr
miniture_port += 1
Smith = Agent((miniture_host, miniture_port))
c = Client(("localhost", config.supervisor_port))


# c.add(5)
# sleep(0.5)
# print Smith.fetch()

# c.reduce(3)
# sleep(0.5)
# print Smith.fetch()

# c.restart([1212])
# print Smith.fetch()

c.stop([1215])
print Smith.fetch()
