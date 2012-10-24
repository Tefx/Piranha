import sys; sys.path.append("../")
from Piranha import config, TYPE_TASKQUEUE, TYPE_PROJECT
from Thinkpol import Agent

import networkx as nx
import matplotlib.pyplot as plt

Smith = Agent(config.miniture_addr_for_agent)


def anlysis(d):
    G = nx.Graph()
    G.add_node("/")
    add_item(G, d, True)
    return G

def add_item(G, d, top=False):
    for k,v in d.iteritems():
        if k == "*": continue
        if top:
            G.add_edge("/", k)
        if isinstance(v, dict):
            for k0 in v.iterkeys():
                G.add_node(k0)
                G.add_edge(k, k0)
            add_item(G, v)
        else:
            G.add_node(k)

def get_dict(agent):
    objs = agent.fetch()
    for k,v in objs.iteritems():
        if k.startswith("RootProject"):
            return v["structure"]

if __name__ == '__main__':
    d = get_dict(Smith)
    g = anlysis(d)
    nx.draw(g)
    plt.show()
