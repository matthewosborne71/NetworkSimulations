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

def PowerLaw(n,exponent):
    DegDist = np.array([1,0])

    while sum(DegDist)%2 == 1:
        DegDist = nx.utils.powerlaw_sequence(n,exponent=exponent)
        DegDist = [int(i) for i in DegDist]

    G = nx.configuration_model(DegDist)
    G = nx.Graph(G)
    G.remove_edges_from(G.selfloop_edges())
    return G

def NegativeBinomial(n,p,num_succ):
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

def GridGraph(m,n,periodic):
    return nx.grid_2d_graph(m,n,periodic)

def RandomRegularGraph(d,n,seed = 'None'):
    if seed == 'None':
        return nx.random_regular_graph(d,n)
    else:
        return nx.random_regular_graph(d,n,seed)
