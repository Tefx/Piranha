#!/usr/bin/env python

import sys;sys.path.append("../")
from Piranha import config
from Corellia import Worker
from Piranha import Supervisor

Worker(Supervisor, "yes", config.miniture_addr).run_alone(config.supervisor_port)