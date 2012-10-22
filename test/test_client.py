import sys; sys.path.append("../")
from time import sleep

from Piranha import Client, config

if __name__ == '__main__':


    def add(x, y):
        return x+y

    def double(x):
        return x*2



    c = Client(config.queuepool_addr, "/")
    # c.add_project("C/K")
    # c.test.add_project("another")
    c.test.add.add_workers(1)