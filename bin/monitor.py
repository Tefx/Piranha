#!/usr/bin/env python

import sys;sys.path.append("../")
import config
from Thinkpol import Miniture

Miniture().run(config.miniture_addr[1], config.miniture_addr[1]+1)