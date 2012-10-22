#!/usr/bin/env python

import sys;sys.path.append("../")
from Piranha import config
from Corellia import Worker
from Piranha import Project


Worker(Project, "root", config.redis_conf, True).run_alone(config.queuepool_port)