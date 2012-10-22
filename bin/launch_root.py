#!/usr/bin/env python

import sys;sys.path.append("../")
from Piranha import config
from Corellia import Worker
from Piranha import RootProject


Worker(RootProject, config.redis_conf).run_alone(config.queuepool_port)