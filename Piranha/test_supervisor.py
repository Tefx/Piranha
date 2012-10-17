import sys;sys.path.append("../")
from Piranha import config
from Corellia import Client
from Thinkpol import Agent
from gevent import sleep

miniture_host, miniture_port = config.miniture_addr
miniture_port += 1
Smith = Agent((miniture_host, miniture_port))
c = Client(("localhost", config.supervisor_port))


c.add(4)
# c.stop([2138])
# c.reduce(2)
sleep(1)
print Smith.fetch()
