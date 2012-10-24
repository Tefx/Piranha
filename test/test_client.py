import sys; sys.path.append("../")
from time import sleep

from Piranha import Client, config

if __name__ == '__main__':

    c = Client(config.rootproject_addr, "/")

    # c.uce.eval.add_workers(1)
    # c.uce.reg_mod.add_workers(1)

    # c.uce.eval.delete_workers(1)
    # c.uce.reg_mod.delete_workers(1)

    # c.uce.delete("eval")
    # c.uce.delete("reg_mod")
    # c.delete("uce")

    c.test_mod.test.add_workers(1)