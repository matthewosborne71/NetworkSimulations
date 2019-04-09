###############################################################################
## CreateNetworks.py                                                         ##
###############################################################################
## Matthew Osborne                                                           ##
## January 20, 2019                                                          ##
###############################################################################
## This code will contain functions for creating various networks for running##
## network simulations.                                                      ##
###############################################################################
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as r
import sys

# This function uses networkx's erdos_renyi_graph function to create an Erdos -
# Renyi graph object. There are n nodes, the probability of an edge between two
# nodes is p, and you can input a seed, the default is 440
def Erdos(n,p,seed = "None"):
    if seed != "None":
        G = nx.erdos_renyi_graph(n,p,seed=seed)
    else:
        G = nx.erdos_renyi_graph(n,p)

    return G

# This function uses networkx's watts_strogaz_graph function to create a Small
# World graph object. There are n nodes, each node is joined with its k nearest
# neighbors in a ring topology, p is the probability of rewiring each edge, you
# can input a seed, the default is 440
def SmallWorld(n,k,p,seed = "None"):
    if seed != "None":
        G = nx.watts_strogatz_graph(n,k,p,seed = seed)
    else:
        G = nx.watts_strogatz_graph(n,k,p)

    return G

def SmallWorldNewman(n,k,p,seed = "None"):
    if seed != "None":
        G = nx.newman_watts_strogatz_graph(n,k,p,seed = seed)
    else:
        G = nx.newman_watts_strogatz_graph(n,k,p)

    return G

# This function will use networkx to read in the edgelist of the SNAP Facebook
# network and create a networkx graph object. Note this requires the file,
# facebook_combined.txt
def SNAPFacebook():
    G = nx.read_edgelist("facebook_combined.txt",create_using=nx.Graph(),
                        nodetype = int)

    return G

def Block(sizes,probs,seed = "None"):
    if seed != "None":
        G = nx.stochastic_block_model(sizes,probs,seed = seed)
    else:
        G = nx.stochastic_block_model(sizes,probs)

    return G

def PowerLaw(n,exponent,seed = "None"):
    if seed != "None":
        np.random.seed(seed)

    DegDist = np.array([1,0])

    while sum(DegDist)%2 == 1:
        DegDist = nx.utils.powerlaw_sequence(n,exponent=exponent)
        DegDist = [int(i) for i in DegDist]

    G = nx.configuration_model(DegDist)
    G = nx.Graph(G)
    G.remove_edges_from(G.selfloop_edges())
    return G

def NegativeBinomial(n,p,num_succ,seed = "None"):
    if seed != "None":
        np.random.seed(seed)
        
    DegDist = np.array([1,0])

    while sum(DegDist) % 2 ==1:
        DegDist = r.negative_binomial(num_succ,p,size = n)
        DegDist = [int(i) for i in DegDist]

    G = nx.configuration_model(DegDist)
    G = nx.Graph(G)
    G.remove_edges_from(G.selfloop_edges())
    return G

def BarabasiAlbert(n,m,seed = 'None'):
    if seed == 'None':
        return nx.barabasi_albert_graph(n,m)
    else:
        return nx.barabasi_albert_graph(n,m,seed)

def TriangularGridGraph(m,n,periodic):
    # Note m is number of columns of triangles
    # n is number of rows of triangles
    # To get the number of nodes in the network we have the following
    # n - odd, m - odd: (m+1)/2 * (n+2)
    # n - odd, m - even: (m/2 + 1) * ((n+1)/2 + 1) + (m/2) * ((n+1)/2)
    # n - even, m - either: (m+1) * (n+2/2)
    return nx.triangular_lattice_graph(m,n,periodic)

def GridGraph(dim,periodic):
    return nx.grid_graph(dim,periodic)

def RandomRegularGraph(d,n,seed = 'None'):
    if seed == 'None':
        return nx.random_regular_graph(d,n)
    else:
        return nx.random_regular_graph(d,n,seed)

def RandomLobster(n,p1,p2,seed = 'None'):
    if seed == 'None':
        return nx.random_lobster(n,p1,p2)
    else:
        return nx.random_lobster(n,p1,p2,seed)
