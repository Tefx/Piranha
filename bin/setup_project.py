#!/usr/bin/env python

import sys; sys.path.append("../")
from types import FunctionType
import os
from sys import argv
from Piranha import config
from Corellia import Client


def parse_file(filename):
    g = {}
    execfile(filename, g)
    mods = g["mods"]
    return {k:v for k,v in g.iteritems() if k in mods}

def make_path(root, filename, k):
    r = "/".join([root.rstrip("/"), os.path.splitext(filename)[0], k])
    return r.lstrip("/")


if __name__ == '__main__':
    filename = argv[1]
    root = "/"
    project = "/".join([root.rstrip("/"), os.path.splitext(filename)[0]]).lstrip("/")
    p = {make_path("/", filename, k):v for k,v in parse_file(filename).iteritems()}
    c = Client(config.rootproject_addr)
    print "adding project:", project
    c.add_project(project)
    for n,f in p.iteritems():
        print "adding task:", n 
        c.add_task(n, f)