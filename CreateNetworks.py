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
import numpy as np
import numpy.random as r
import sys

# This function uses networkx's erdos_renyi_graph function to create an Erdos -
# Renyi graph object. There are n nodes, the probability of an edge between two
# nodes is p, and you can input a seed, the default is 440
def Erdos(n,p):
    print "Make Graph"
    G = nx.erdos_renyi_graph(n,p)

    return G

# This function uses networkx's watts_strogaz_graph function to create a Small
# World graph object. There are n nodes, each node is joined with its k nearest
# neighbors in a ring topology, p is the probability of rewiring each edge, you
# can input a seed, the default is 440
def SmallWorld(n,k,p):
    print "Make Graph"
    G = nx.watts_strogatz_graph(n,k,p)

    return G

# This function will return a configuration model of size n using networkx.
# We'll use random or networkx to create a degree distribution of DistType. This
# is then fed into the networkx function. You can input a seed, the default is
# 440. DistType: "Binomial", "PowerLaw", "NegativeBinomial", "Poisson", "Exponential"
def Configuration(n,DistType):
    print "Making the degree distribution."
    DegDist = np.array([1,0])
    if DistType == "Binomial":
        numTrials = int(raw_input("You want a binomial with how many trials? "))
        prob = float(raw_input("What probability of success do you want? "))

        while sum(DegDist) % 2 ==1:
            DegDist = r.binomial(numTrials,prob,size = n)


    elif DistType == "PowerLaw":
        exponent = float(raw_input("What do you want the power law exponent to be? "))

        while sum(DegDist)%2 == 1:
            DegDist = nx.utils.powerlaw_sequence(n,exponent=exponent)
            DegDist = map(int,DegDist)

    elif DistType == "NegativeBinomial":
        num_failures = int(raw_input("You want a negative binomial with how many failures? "))
        prob = float(raw_input("What probability of success? "))

        while sum(DegDist) % 2 ==1:
            DegDist = r.negative_binomial(num_failures,prob,size = n)

    elif DistType == "Poisson":
        lam = float(raw_input("What should the lambda parameter be of your Poisson? "))

        while sum(DegDist) % 2 == 1:
            DegDist = r.poisson(lam,size = n)

    elif DistType == "Exponential":
        beta = float(raw_input("What should the scale parameter be of your Exponential? "))

        while sum(DegDist) % 2 == 1:
            DegDist = r.exponential(beta,size = n)

    print "Making the graph now"
    G = nx.configuration_model(DegDist)

    return G

# This function will take in a graph and node positions and then output a plot
# of the graph
def DrawGraph(G,node_size=5,width = .3):
    print "Fetching Positions"
    pos = nx.spring_layout(G)

    print "Initializing Figure"
    plt.figure(figsize = (15,15))

    print "Drawing nodes"
    nx.draw_networkx_nodes(G,pos,node_size=node_size)

    print "Drawing edges, this may take a while"
    nx.draw_networkx_edges(G,pos,width=width)

    plt.show()
