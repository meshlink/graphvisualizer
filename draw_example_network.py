"""
Draw a graph, colour the nodes and edges based on their class, and overlay
the routing spanning tree.

Requires matplotlib and networkx.
It's best to install matplotlib through 'apt-get install python-matplotlib'
as it depends on numpy, scipy, and some other packages that are hard to build.
"""

try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
import random

class DeviceClass(object):
    def __init__(self, name, weight, color):
        self.name = name
        self.weight = weight
        self.color = color
        self.edges = list()


device_classes = list([
    DeviceClass('backbone', 1, 'w'),
    DeviceClass('server', 2, 'g'),
    DeviceClass('desktop', 3, 'y'),
    DeviceClass('mobile', 4, 'r'),
])
node_classes = dict()

# random graph
G = nx.random_regular_graph(3, 30)

# assign random class to each node
for n in G.nodes():
    node_classes[n] = random.choice(device_classes)

# assign weights to edges based on the two nodes' classes
for (u,v,d) in G.edges(data=True):
    u_cls = node_classes[u]
    v_cls = node_classes[v]
    d_cls = u_cls if u_cls.weight > v_cls.weight else v_cls
    d['weight'] = d_cls.weight
    d_cls.edges.append((u,v))

pos=nx.spring_layout(G) # positions for all nodes

# draw nodes individually to color them nicely
for n in G.nodes():
    nx.draw_networkx_nodes(G,pos,nodelist=[n],node_color=node_classes[n].color,node_size=300)

# draw edges
edge_size_offset = max(device_classes, key=lambda x: x.weight).weight + 1
for cls in device_classes:
    nx.draw_networkx_edges(G, pos, edgelist=cls.edges, width=(edge_size_offset - cls.weight), alpha=1, edge_color=cls.color)

# build the spanning tree
SP = nx.algorithms.mst.minimum_spanning_tree(G)

# draw spanning tree edges
nx.draw_networkx_edges(G, pos, edgelist=SP.edges(), width=4, alpha=1, edge_color='black', style='dashed')
    
nx.draw_networkx_labels(G,pos,font_size=8,font_family='sans-serif')

plt.axis('off')
plt.savefig("weighted_graph.png") # save as png
plt.show() # display

