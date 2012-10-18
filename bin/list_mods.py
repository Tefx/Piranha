#!/usr/bin/env python

import sys;sys.path.append("../")
import config
from Thinkpol import Agent

miniture_host, miniture_port = config.miniture_addr
miniture_port += 1
Smith = Agent((miniture_host, miniture_port))

info = Smith.fetch()
for worker in info:
    print "%s: %s" % (worker, ", ".join(info[worker]["mods"]))