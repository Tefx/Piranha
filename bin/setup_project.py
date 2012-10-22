import sys; sys.path.append("../")
from types import FunctionType
import os
from sys import argv
from Piranha import config
from Corellia import Client


def parse_file(filename):
    g = {}
    execfile(filename, g)
    return {k:v for k,v in g.iteritems() if isinstance(v, FunctionType)}

def make_path(root, filename, k):
    r = "/".join([root.rstrip("/"), os.path.splitext(filename)[0], k])
    return r.lstrip("/")


if __name__ == '__main__':
    filename = argv[1]
    root = "/"
    project = "/".join([root.rstrip("/"), os.path.splitext(filename)[0]]).lstrip("/")
    p = {make_path("/", "tt.py", k):v for k,v in parse_file(filename).iteritems()}
    c = Client(config.queuepool_addr)
    print "adding project:", project
    c.add_project(project)
    for n,f in p.iteritems():
        print "adding task:", n 
        c.add_task(n, f)


    # mean = lambda l: sum(l)/len(l)

    # def m7(p, A, P, p_0):
    #     n = len(A)
    #     p = p * (n/len(p))
    #     p_ = mean(p)
    #     A_= mean(A)
    #     Sxy = sum([(p0-p_)*(A0-A_) for p0, A0 in zip(p, A)])
    #     Sxx = sum([(p0-p_)**2 for p0 in p])
    #     b = Sxy/Sxx
    #     a = A_ - b*p_
    #     s = sqrt(sum([(A0-a-b*p0)**2 for A0, p0 in zip(A, p)])/(n-2))
    #     u_p0 = s/b*sqrt(1/P+1/n+(p_0-p_)**2/Sxx)
    #     return u_p0/p_0

    # from Husky import dumps, loads
    # # print [isinstance(f, FunctionType) for f in mean.func_code.co_names]
    # b = dumps(m7)
    # print loads(b)