#!/usr/bin/env python

import sys; sys.path.append("../")
from Thinkpol import Agent
from Piranha import config, TYPE_TASKQUEUE, TYPE_PROJECT


def join_path(p, n):
    return "/".join([p.strip("/"), n.strip("/")])

def draw_tree(d, gd, path="", show_workers=True):
    for k,v in d.iteritems():
        if k == "*":
            continue
        else:
            v_path = join_path(path, k)
            if isinstance(v, dict):
                yield "%s:" % k
                for i in draw_tree(v, gd, v_path):
                    yield "  "+i
            elif v == TYPE_PROJECT:
                yield "%s: EmptyProject" % k
            elif v == TYPE_TASKQUEUE:
                yield "%s: %s" % (k, find_tq(v_path, gd))
                if show_workers:
                    workers = [i for i in find_workers(v_path, gd)]
                    if workers:
                        yield "    => Workers: %d" % len(workers)
                        for w in workers:
                            yield "       %s" % w
                    else:
                        yield "    => No Worker"

def find_tq(path, d):
    for k,v in d.iteritems():
        if k.startswith("TaskQueue") and v["path"] == path:
            return k

def find_workers(path, d):
    for k,v in d.iteritems():
        if k.startswith("Worker") and (v["path"] == path or path == join_path("root", v["path"])):
            yield k

def find_structure(d):
    for k,v in d.iteritems():
        if k.startswith("RootProject"):
            return {"root": v["structure"]}

if __name__ == '__main__':
    Smith = Agent(config.miniture_addr_for_agent)
    gd = Smith.fetch()
    structure = find_structure(gd)
    print "\n".join(draw_tree(structure, gd, show_workers=True))