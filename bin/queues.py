#!/usr/bin/env python

import sys;sys.path.append("../")
from Piranha import config
from Corellia import Worker
from Piranha import QueuePool

Worker(QueuePool, config.queuesconfig).run_alone(config.queuepool_port)