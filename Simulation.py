###############################################################################
## Simulation.py                                                             ##
###############################################################################
## Matthew Osborne                                                           ##
## July 30, 2018                                                             ##
###############################################################################
## Code that will run network simulations of disease spread                  ##
## network simulations.                                                      ##
###############################################################################

import networkx as nx
import CreateNetworks as CN
import random
import matplotlib.pyplot as plt

# Update Edges will update the edges of the network after infection or recovery
def UpdateEdges(G,SIEdges,Node,Type):
    # For each edge involving the Node
    for node in G[Node]:

        # Write down the edge
        if node < Node:
            edge = (node,Node)
        else:
            edge = (Node,node)

        # If Node recovered
        if Type == "S":
            if G.nodes[node]['Status'] == "S":
                SIEdges.remove(edge)
                Update = "SS"
            elif G.nodes[node]['Status'] == "I":
                SIEdges.add(edge)
                Update = "SI"

        # If Node got infected
        elif Type == "I":
            if G.nodes[node]['Status'] == "S":
                SIEdges.add(edge)
                Update = "SI"
            elif G.nodes[node]['Status'] == "I":
                SIEdges.remove(edge)
                Update = "II"

        G[Node][node]['Type'] = Update

    return G,SIEdges


# Infect will infect an "at risk" node by randomly selecting an SI edge
def InitialInfect(G,Infected):
    Susceptible = set(G.nodes.keys()) - Infected
    node = random.sample(Susceptible,1)[0]
    Infected.add(node)
    G.nodes[node]['Status'] = "I"
    print "Infected Node " + str(node)
    return node,G,Infected


# Recover will recover a randomly selected infected node
def Recover(G,Infected):
    node = random.sample(Infected,1)[0]
    Infected.remove(node)
    print str(node) + " recovered"
    G.nodes[node]['Status'] = "S"
    return node,G,Infected

def Infect(G,Infected,SIEdges):
    edge = random.sample(SIEdges,1)[0]
    for item in edge:
        if G.nodes[item]['Status'] == "S":
            node = item
            Infected.add(item)

    print str(node) + " infected"
    G.nodes[node]['Status'] = "I"
    return node,G,Infected


# Will calculate the overall reaction rate
def CalculateRate(SIEdges,Infected,beta,gamma):
    rate = beta*len(SIEdges) + gamma*len(Infected)
    return rate

def WhatHappened(Infected,rate,gamma):
    u = random.uniform(0,rate)
    if u < gamma*len(Infected):
        event = "Recovery"
    else:
        event = "Infection"

    return event

def SimpleSim(G,InitialFrac,StoppingTime,gamma,beta):

# Initial Parameters
# Size = 1000
# EdgeProb = 1
# InitialFrac = .1
# StoppingTime = 5
# gamma = 900
# beta = 1

    # Set all the nodes to susceptible
    nx.set_node_attributes(G,"S",'Status')

    # Set all the edges to SS
    nx.set_edge_attributes(G,"SS",'Type')

    Infected = set([])
    SIEdges = set([])


    InfectSeed = int(InitialFrac * len(G.nodes))

    # Infect the patient zeroes
    print "Initial Infection"
    for i in range(InfectSeed):
        node,G,Infected = InitialInfect(G,Infected)
        G,SIEdges = UpdateEdges(G,SIEdges,node,"I")

    CurrentTime = 0
    Time = [CurrentTime]
    CurrentInfected = [len(Infected)]

    WaitingTimes = []
    Events = []

    while (CurrentTime < StoppingTime) & (len(Infected) > 0):
        # Find the time until the next event
        rate = CalculateRate(SIEdges,Infected,beta,gamma)
        WaitingTime = random.expovariate(rate)
        WaitingTimes.append(WaitingTime)

        Event = WhatHappened(Infected,rate,gamma)
        Events.append(Event)

        print Event + " happend at " + str(CurrentTime+WaitingTime)

        if Event == "Recovery":
            ChangedNode,G,Infected = Recover(G,Infected)
            Type = "S"
        elif Event == "Infection":
            ChangedNode,G,Infected = Infect(G,Infected,SIEdges)
            Type = "I"

        G,SIEdges = UpdateEdges(G,SIEdges,ChangedNode,Type)

        CurrentTime = CurrentTime + WaitingTime

        Time.append(CurrentTime)
        CurrentInfected.append(len(Infected))
        print CurrentTime < StoppingTime
        print len(Infected) > 0
        print len(Time)

    plt.plot(Time,CurrentInfected)
    plt.show()

    #return Time,CurrentInfected
