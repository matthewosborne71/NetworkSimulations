###############################################################################
## Simulation.py                                                             ##
###############################################################################
## Matthew Osborne                                                           ##
## January 20, 2019                                                          ##
###############################################################################
## Code that will run network simulations of disease spread                  ##
## network simulations.                                                      ##
###############################################################################

import networkx as nx
import CreateNetworks as CN
import random
import matplotlib.pyplot as plt

# For complex contagion simulations. Takes in a node and checks if it has
# passed the at risk threshold
def IsAtRisk(G,Node,ThresholdType):
    INeighbors = 0
    for edge in G[Node]:
        if G[Node][edge]['Type'] == "SI":
            INeighbors = INeighbors + 1

    if ThresholdType == "Num":
        if INeighbors >= G.nodes[Node]['Threshold']:
            return True
        else:
            return False
    elif ThresholdType == "Frac":
        if len(G[Node]) == 0:
            return False
        elif float(INeighbors)/float(len(G[Node])) >= G.nodes[Node]['Threshold']:
            return True
        else:
            return False

# If the simulation is of a complex contagion we need to update the at risk
# edges. This function does that
def UpdateAtRisk(G,AtRiskEdges,Node,UpdateType,ThresholdType):
    AddAtRiskEdges = set([])
    RemoveAtRiskEdges = set([])

    if UpdateType == "I":
        for neighbor in G[Node]:
            if G[Node][neighbor]['Type'] == "SI":
                if IsAtRisk(G,neighbor,ThresholdType):
                    for edge in G[neighbor]:
                        if G[neighbor][edge]['Type'] == "SI":
                            G[neighbor][edge]['AtRisk'] = "Yes"
                            if edge < neighbor:
                                E = (edge,neighbor)
                            else:
                                E = (neighbor,edge)
                            AddAtRiskEdges.add(E)
            else:
                G[Node][neighbor]['AtRisk'] = "No"
                if neighbor < Node:
                    edge = (neighbor,Node)
                else:
                    edge = (Node,neighbor)
                if edge in AtRiskEdges:
                    RemoveAtRiskEdges.add(edge)

        if len(RemoveAtRiskEdges) > 0:
            for node in RemoveAtRiskEdges:
                AtRiskEdges.remove(node)
        if len(AddAtRiskEdges) > 0:
            for node in AddAtRiskEdges:
                AtRiskEdges.add(node)

    elif UpdateType == "S":
        for neighbor in G[Node]:
            if G.nodes[neighbor]['Status'] == "S":
                if G[Node][neighbor]["AtRisk"] == "Yes":
                    G[Node][neighbor]["AtRisk"] = "No"
                    if neighbor < Node:
                        RemoveAtRiskEdges.add((neighbor,Node))
                    else:
                        RemoveAtRiskEdges.add((Node,neighbor))

                    if IsAtRisk(G,neighbor,ThresholdType) == False:
                        for edge in G[neighbor]:
                            if G[neighbor][edge]['AtRisk']=="Yes":
                                G[neighbor][edge]['AtRisk'] = "No"
                                if neighbor < edge:
                                    RemoveAtRiskEdges.add((neighbor,edge))
                                else:
                                    RemoveAtRiskEdges.add((edge,neighbor))

        if IsAtRisk(G,Node,ThresholdType):
            for edge in G[Node]:
                if G[Node][edge]['Type'] == "SI":
                    G[Node][edge]['AtRisk'] = "Yes"
                    if edge < Node:
                        AddAtRiskEdges.add((edge,Node))
                    else:
                        AddAtRiskEdges.add((Node,edge))

        if len(RemoveAtRiskEdges) > 0:
            for node in RemoveAtRiskEdges:
                AtRiskEdges.remove(node)
        if len(AddAtRiskEdges) > 0:
            for node in AddAtRiskEdges:
                AtRiskEdges.add(node)
    return G,AtRiskEdges




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
    return node,G,Infected

def InitialBlockInfect(G,Partitions,Infected):
    Susceptible = set.union(*Partitions) - Infected
    node = random.sample(Susceptible,1)[0]
    Infected.add(node)
    G.nodes[node]['Status'] = "I"
    return node,G,Infected



# Recover will recover a randomly selected infected node
def Recover(G,Infected):
    node = random.sample(Infected,1)[0]
    Infected.remove(node)
    G.nodes[node]['Status'] = "S"
    return node,G,Infected

def Infect(G,Infected,SIEdges):
    edge = random.sample(SIEdges,1)[0]
    for item in edge:
        if G.nodes[item]['Status'] == "S":
            node = item
            Infected.add(item)

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
    for i in range(InfectSeed):
        node,G,Infected = InitialInfect(G,Infected)
        G,SIEdges = UpdateEdges(G,SIEdges,node,"I")

    CurrentTime = 0
    Time = [CurrentTime]
    CurrentInfected = [len(Infected)]

    WaitingTimes = []
    Events = ["Start"]
    rate = 1

    while (CurrentTime < StoppingTime) & (len(Infected) > 0) & (rate > 0):
        # Find the time until the next event
        rate = CalculateRate(SIEdges,Infected,beta,gamma)
        #print(rate)
        WaitingTime = random.expovariate(rate)
        WaitingTimes.append(WaitingTime)

        Event = WhatHappened(Infected,rate,gamma)
        Events.append(Event)


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
        rate = CalculateRate(SIEdges,Infected,beta,gamma)

    return Time,Events,CurrentInfected

def ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,Threshold,ThresholdType):
    # Set all the nodes to susceptible
    nx.set_node_attributes(G,"S",'Status')

    # Set all the nodes threshold
    nx.set_node_attributes(G,Threshold,'Threshold')

    # Set all the edges to SS
    nx.set_edge_attributes(G,"SS",'Type')

    # Set all edges to not at risk
    nx.set_edge_attributes(G,"No",'AtRisk')

    Infected = set([])
    SIEdges = set([])
    AtRiskEdges = set([])

    InfectSeed = int(InitialFrac * len(G.nodes))


    for i in range(InfectSeed):
        node,G,Infected = InitialInfect(G,Infected)
        G,SIEdges = UpdateEdges(G,SIEdges,node,"I")
        G,AtRiskEdges = UpdateAtRisk(G,AtRiskEdges,node,"I",ThresholdType)

    CurrentTime = 0
    Time = [CurrentTime]
    CurrentInfected = [len(Infected)]

    WaitingTimes = []
    Events = ["Start"]

    while (CurrentTime < StoppingTime) & (len(Infected) > 0):
        # print "Nodes " +str(nx.get_node_attributes(G,"Status"))
        # print "Infected:" + str(Infected)
        # print "SI: " + str(SIEdges)
        # print "AtRisk: " + str(AtRiskEdges)
        # print "Status, AtRisk: " + str(nx.get_edge_attributes(G,"AtRisk"))
        # print "Status, SI:" + str(nx.get_edge_attributes(G,"Type"))
        # print "\n\n\n"

        rate = CalculateRate(AtRiskEdges,Infected,beta,gamma)
        WaitingTime = random.expovariate(rate)
        WaitingTimes.append(WaitingTime)

        Event = WhatHappened(Infected,rate,gamma)
        Events.append(Event)

        if Event == "Recovery":
            ChangedNode,G,Infected = Recover(G,Infected)
            Type = "S"
        elif Event == "Infection":
            ChangedNode,G,Infected = Infect(G,Infected,AtRiskEdges)
            Type = "I"

        G,SIEdges = UpdateEdges(G,SIEdges,ChangedNode,Type)
        G,AtRiskEdges = UpdateAtRisk(G,AtRiskEdges,ChangedNode,Type,ThresholdType)

        CurrentTime = CurrentTime + WaitingTime

        Time.append(CurrentTime)
        CurrentInfected.append(len(Infected))
        # print CurrentTime < StoppingTime
        # print len(Infected) > 0
        # print len(Time)
        # print (CurrentTime < StoppingTime) & (len(Infected) > 0)
        # print CurrentTime
        #
        # print "\n\n\n"
        #
        # print "Nodes " +str(nx.get_node_attributes(G,"Status"))
        # print "Infected:" + str(Infected)
        # print "SI: " + str(SIEdges)
        # print "AtRisk: " + str(AtRiskEdges)
        # print "Status, AtRisk: " + str(nx.get_edge_attributes(G,"AtRisk"))
        # print "Status, SI:" + str(nx.get_edge_attributes(G,"Type"))


    return Time,Events,CurrentInfected

def SimpleBlockSim(G,InitialFrac,WhereInfect,StoppingTime,gamma,beta):

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

    Partitions = []
    for i in WhereInfect:
        Partitions.append(G.graph['partition'][i])


    InfectSeed = int(InitialFrac * len(G.nodes))

    # Infect the patient zeroes
    for i in range(InfectSeed):
        node,G,Infected = InitialBlockInfect(G,Partitions,Infected)
        G,SIEdges = UpdateEdges(G,SIEdges,node,"I")

    del Partitions

    NPartitions = len(G.graph['partition'])

    PartitionInfected = []

    for i in range(NPartitions):
        PartitionInfected.append([])
        PartitionInfected[i].append(len(Infected.intersection(G.graph['partition'][i])))

    CurrentTime = 0
    Time = [CurrentTime]
    CurrentInfected = [len(Infected)]

    WaitingTimes = []
    Events = ["Start"]
    rate = 1

    while (CurrentTime < StoppingTime) & (len(Infected) > 0) & (rate > 0):
        # Find the time until the next event
        rate = CalculateRate(SIEdges,Infected,beta,gamma)
        #print(rate)
        WaitingTime = random.expovariate(rate)
        WaitingTimes.append(WaitingTime)

        Event = WhatHappened(Infected,rate,gamma)
        Events.append(Event)


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
        for i in range(NPartitions):
            PartitionInfected[i].append(len(Infected.intersection(G.graph['partition'][i])))
        rate = CalculateRate(SIEdges,Infected,beta,gamma)

    return Time,Events,CurrentInfected,PartitionInfected
