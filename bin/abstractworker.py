#!/usr/bin/env python

import sys;sys.path.append("../")
from Piranha import MutableWorker, config, MutableWorker
from Thinkpol import Telescreen
from os import getpid
import psutil

class AbstractWorker(MutableWorker, Telescreen):
    monitoring = ["mods", "pid"]

    def __init__(self, miniture_addr):
        super(AbstractWorker, self).__init__()
        self.p = psutil.Process(getpid())
        self.pid = self.p.pid
        self._connect(miniture_addr)

AbstractWorker(config.miniture_addr).run((config.queuepool_host, config.queuepool_port), "common")