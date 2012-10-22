#!/usr/bin/env python

import sys;sys.path.append("../")
from Piranha import Worker, config

Worker(config.queuepool_addr).run()