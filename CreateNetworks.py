###############################################################################
## CreateNetworks.py                                                         ##
###############################################################################
## Matthew Osborne                                                           ##
## June 4, 2018                                                              ##
###############################################################################
## This code will contain functions for creating various networks for running##
## network simulations.                                                      ##
###############################################################################
import networkx as nx
import matplotlib.pyplot as plt

# This function uses networkx's erdos_renyi_graph function to create an Erdos -
# Renyi graph object. There are n nodes, the probability of an edge between two
# nodes is p, and you can input a seed, the default is 440
def Erdos(n,p,seed=440):
    print "Make Graph"
    G = nx.erdos_renyi_graph(n,p,seed=seed)


    print "Fetching Positions"
    pos = nx.spring_layout(G)

    return G,pos

def SmallWorld(n,k,p,seed=440):
    print "Make Graph"
    G = nx.watts_strogatz_graph(n,k,p,seed=seed)

    print "Fetching Positions"
    pos = nx.spring_layout(G)

    return G,pos


# This function will take in a graph and node positions and then output a plot
# of the graph
def DrawGraph(G,pos,node_size=5,width = .3):
    print "Initializing Figure"
    plt.figure(figsize = (15,15))

    print "Drawing nodes"
    nx.draw_networkx_nodes(G,pos,node_size=node_size)

    print "Drawing edges, this may take a while"
    nx.draw_networkx_edges(G,pos,width=width)

    plt.show()
