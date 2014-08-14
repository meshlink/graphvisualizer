"""
Draw a graph, color the nodes and edges based on their class, and overlay
the routing spanning tree. For the spanning tree, the maximum weight
of two directed edges is used for the single directed edge.

Takes a single json file as input and generates a png file of the graph.
the json file is expected to have the following format, by example:
{
        "nodes": {
                "machine1node0": {
                        "name": "machine1node0",
                        "options": 50331652,
                        "devclass": 0
                },
                "machine1node1": {
                        "name": "machine1node1",
                        "options": 0,
                        "devclass": 1
                },
                "machine1node2": {
                        "name": "machine1node2",
                        "options": 50331652,
                        "devclass": 2
                },
                "machine1node3": {
                        "name": "machine1node3",
                        "options": 50331652,
                        "devclass": 0
                },
                "machine1node4": {
                        "name": "machine1node4",
                        "options": 0,
                        "devclass": 1
                },
                "machine1node5": {
                        "name": "machine1node5",
                        "options": 0,
                        "devclass": 2
                },
                "machine1node6": {
                        "name": "machine1node6",
                        "options": 0,
                        "devclass": 0
                },
                "machine1node7": {
                        "name": "machine1node7",
                        "options": 0,
                        "devclass": 1
                },
                "machine1node8": {
                        "name": "machine1node8",
                        "options": 0,
                        "devclass": 2
                },
                "machine1node9": {
                        "name": "machine1node9",
                        "options": 0,
                        "devclass": 0
                }
        },
        "edges": {
                "machine1node0_to_machine1node3": {
                        "from": "machine1node0",
                        "to": "machine1node3",
                        "address": { "host": "127.0.0.1", "port": 22643 },
                        "options": 50331652,
                        "weight": 1
                },
                "machine1node2_to_machine1node0": {
                        "from": "machine1node2",
                        "to": "machine1node0",
                        "address": { "host": "127.0.0.1", "port": 21863 },
                        "options": 50331652,
                        "weight": 1
                },
                "machine1node3_to_machine1node0": {
                        "from": "machine1node3",
                        "to": "machine1node0",
                        "address": { "host": "127.0.0.1", "port": 21863 },
                        "options": 50331652,
                        "weight": 1
                },
                "machine1node0_to_machine1node2": {
                        "from": "machine1node0",
                        "to": "machine1node2",
                        "address": { "host": "127.0.0.1", "port": 10345 },
                        "options": 50331652,
                        "weight": 6
                }
        }
}

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
import sys
import json
import pickle


class DeviceClass(object):
    def __init__(self, name, weight, color):
        self.name = name
        self.weight = weight
        self.color = color
        self.edges = list()


class Node(object):
    def __init__(self, name, options, devclass):
        self.name = name
        self.options = options
        self.devclass = devclass


class Edge(object):
    def __init__(self, name, from_node, to_node, address, options, weight):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.address = address
        self.options = options
        self.weight = weight


def get_edge_name(from_name, to_name):
    return "{} to {}".format(from_name, to_name)

def build_objects_from_data(data, device_class_dict):
    """
    Turn the parsed data into actual objects. Does a bit of data validation.
    Returns a dictionary
    {
        'nodes': map_of_name_to_node_instances,
        'edges': map_of_name_to_edge_instances,
    }
    """
    node_names_set = set()
    nodes = dict()
    edges = dict()
    for k, v in data['nodes'].items():
        if k != v['name'] or k in node_names_set:
            raise RuntimeError("Data validation error: "\
                "duplicate name or node has different label than name."
            )
        else:
            n = Node(
                v['name'],
                v['options'],
                device_class_dict[v['devclass']],
            )
            nodes[n.name] = n
            node_names_set.add(n.name)
    for k, v in data['edges'].items():
        if v['from'] not in node_names_set or v['to'] not in node_names_set:
            raise RuntimeError("Data validation error: "\
                "edge from or to a node that doesn't exist."
            )
        e = Edge(
            k,
            nodes[v['from']],
            nodes[v['to']],
            v['address'],
            v['options'],
            v['weight'],
        )
        edges[e.name] = e
    return {
        'nodes': nodes,
        'edges': edges,
    }

def main(infile, outfile, position_file=None, bounce=False, prefer_lower_weight_edge=True):
    # not using input right now, just hard-coded to known classes
    device_classes = {
        0: DeviceClass('backbone', 1, 'g'),
        1: DeviceClass('stationaryr', 3, 'y'),
        2: DeviceClass('portable', 6, 'r'),
        3: DeviceClass('unknown', 9, 'b'),
    }

    with open(infile, 'r') as fp:
        data = json.loads(fp.read())
    data = build_objects_from_data(data, device_classes)

    G = nx.DiGraph()
    
    # add nodes to graph
    G.add_nodes_from([n for n in data['nodes'].keys()])

    # add edges to graph and assign them to a device class based on endpoints
    for e in data['edges'].values():
        edge_cls = e.to_node.devclass
        edge_cls.edges.append(e)
        G.add_edge(e.from_node.name, e.to_node.name, weight=e.weight)

    # load existing node positions if possible
    try:
        with open(position_file, 'r') as fp:
            keep = pickle.load(fp)
            if bounce:
                fixed = None
            else:
                fixed = keep.keys()
    except:
        keep = None
        fixed = None

    pos = nx.spring_layout(G, pos=keep, fixed=fixed)

    # write node positions if possible
    if position_file:
        with open(position_file, 'w') as fp:
            pickle.dump(pos, fp)
    
    # draw nodes individually and color them by class
    for node in G.nodes():
        node_color = data['nodes'][node].devclass.color
        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=node_color, node_size=300)

    # draw edges
    edge_size_offset = max(device_classes.values(), key=lambda x: x.weight).weight + 1
    sorted_devclasses = device_classes.values()
    sorted_devclasses.sort(key=lambda x:x.weight, reverse=prefer_lower_weight_edge)
    for cls in sorted_devclasses:
        edgelist = [(e.from_node.name, e.to_node.name) for e in cls.edges]
        nx.draw_networkx_edges(G, pos, edgelist=edgelist, alpha=1, edge_color=cls.color)

    """
    # get undirected graph to build spanning tree and correct the edge weights
    G_undirected = G.to_undirected(reciprocal=True)
    for u, v, d in G_undirected.edges(data=True):
        # TODO this needs to be fixed to use the edge weight no the devclass weight
        u_node = data['nodes'][u]
        v_node = data['nodes'][v]
        if prefer_lower_weight_edge:
            d['weight'] = min(u_node.devclass.weight, v_node.devclass.weight)
        else:
            d['weight'] = max(u_node.devclass.weight, v_node.devclass.weight)


    # get MST
    ST = nx.algorithms.mst.minimum_spanning_tree(G_undirected)

    # make MST edges bi-directional
    st_edges = ST.edges()
    for u, v in ST.edges():
        st_edges.append((v,u))

    # draw spanning tree edges
    nx.draw_networkx_edges(G, pos, edgelist=st_edges, alpha=0.3, edge_color='black', style='dashed')
    """
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    edge_labels = dict()
    for e in data['edges'].values():
        edge_labels[(e.from_node.name, e.to_node.name)] = str(e.weight)
    # label_pos: 0=head, 0.5=middle, 1=tail
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.25, font_size=8, font_family='sans-serif')

    plt.axis('off')
    plt.savefig(outfile) # save as png

if __name__ == "__main__":
    usage = "Usage: {} input_file.json output_file [position_file]\n\n"\
            "input_file.json:   JSON formatted input file\n"\
            "output_file:       output file name (type determined by extension"\
            "position_file:     (optional) temporary file to hold node positions between runs\n"\
            .format(sys.argv[0])

    # parse arguments
    if len(sys.argv) < 3:
        print usage
        sys.exit()
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        position_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    main(infile, outfile, position_file, bounce=True, prefer_lower_weight_edge=True)

