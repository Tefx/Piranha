import sys; sys.path.append("../")
from time import sleep

from Piranha import Client, config

if __name__ == '__main__':

    c = Client(config.queuepool_addr, "/")
    c.uce.eval.add_workers(1)
    c.uce.reg_mod.add_workers(1)