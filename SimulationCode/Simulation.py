###############################################################################
## Simulation.py                                                             ##
###############################################################################
## Matthew Osborne                                                           ##
## January 20, 2019                                                          ##
###############################################################################
## Code that will run network simulations of disease spread                  ##
## network simulations.                                                      ##
###############################################################################

# Import the packages we will use
import networkx as nx
import CreateNetworks as CN
import random
import matplotlib.pyplot as plt

# For complex contagion simulations. Takes in a node and checks if it has
# passed the at risk threshold
def IsAtRisk(G,Node,ThresholdType):
    # Find the number of neighbors that are I
    INeighbors = 0
    for edge in G[Node]:
        if G[Node][edge]['Type'] == "SI":
            INeighbors = INeighbors + 1

    # Check to see if num I is greater than threshold
    if ThresholdType == "Num":
        if INeighbors >= G.nodes[Node]['Threshold']:
            return True
        else:
            return False
    # Check to see if frac of I neighbors is greater than threshold
    elif ThresholdType == "Frac":
        if len(G[Node]) == 0:
            return False
        elif float(INeighbors)/float(len(G[Node])) >= G.nodes[Node]['Threshold']:
            return True
        else:
            return False

# If the simulation is of a complex contagion we need to update the at risk
# edges. This function does that after we have updated the SIedges.
def UpdateAtRisk(G,AtRiskEdges,Node,UpdateType,ThresholdType):
    # This set collects the at risk edges we need to add
    AddAtRiskEdges = set([])

    # This set collects the edges that were at risk that we need to remove
    RemoveAtRiskEdges = set([])

    # Was the event an infection?
    if UpdateType == "I":
        # for each of the Node's neighbors
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

        # Do we need to add or remove any edges
        if len(RemoveAtRiskEdges) > 0:
            for node in RemoveAtRiskEdges:
                AtRiskEdges.remove(node)
        if len(AddAtRiskEdges) > 0:
            for node in AddAtRiskEdges:
                AtRiskEdges.add(node)

    # If Node Recovered
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

# This function will run UpdateAtRisk on a block model.
def UpdateBlockAtRisk(G,AtRiskEdges,Node,UpdateType,ThresholdType):
    # record the block the changed node is in
    Node_block = G.nodes[Node]['block']

    # These keep track of any edges we need to add or remove
    AddAtRiskEdges = set([])
    RemoveAtRiskEdges = set([])

    # if Node was infected
    if UpdateType == "I":
        # For each of the Node's neighbors
        # check to see what edges need to be added or removed
        for neighbor in G[Node]:
            neighbor_block = G.nodes[neighbor]['block']
            if G.nodes[neighbor]['Status'] == "S":
                if IsAtRisk(G,neighbor,ThresholdType):
                    for edge in G[neighbor]:
                        if G[neighbor][edge]['Type'] == "SI":
                            G[neighbor][edge]['AtRisk'] = "Yes"
                            if edge < neighbor:
                                E = (edge,neighbor)
                            else:
                                E = (neighbor,edge)
                            AddAtRiskEdges.add((E,neighbor_block))
            else:
                G[Node][neighbor]['AtRisk'] = "No"
                if neighbor < Node:
                    edge = (neighbor,Node)
                else:
                    edge = (Node,neighbor)
                if edge in AtRiskEdges[Node_block]:
                    RemoveAtRiskEdges.add((edge,Node_block))

        if len(RemoveAtRiskEdges) > 0:
            for pair in RemoveAtRiskEdges:
                AtRiskEdges[pair[1]].remove(pair[0])
        if len(AddAtRiskEdges) > 0:
            for pair in AddAtRiskEdges:
                AtRiskEdges[pair[1]].add(pair[0])
    # If Node Recovered
    elif UpdateType == "S":
        # for each neighbor of Node
        # check to see what edges need to be added or removed
        for neighbor in G[Node]:
            neighbor_block = G.nodes[neighbor]['block']
            if G.nodes[neighbor]['Status'] == "S":
                if G[Node][neighbor]["AtRisk"] == "Yes":
                    G[Node][neighbor]["AtRisk"] = "No"
                    if neighbor < Node:
                        RemoveAtRiskEdges.add(((neighbor,Node),neighbor_block))
                    else:
                        RemoveAtRiskEdges.add(((Node,neighbor),neighbor_block))

                    if IsAtRisk(G,neighbor,ThresholdType) == False:
                        for edge in G[neighbor]:
                            if G[neighbor][edge]['AtRisk']=="Yes":
                                G[neighbor][edge]['AtRisk'] = "No"
                                if neighbor < edge:
                                    RemoveAtRiskEdges.add(((neighbor,edge),neighbor_block))
                                else:
                                    RemoveAtRiskEdges.add(((edge,neighbor),neighbor_block))

        if IsAtRisk(G,Node,ThresholdType):
            for edge in G[Node]:
                if G[Node][edge]['Type'] == "SI":
                    G[Node][edge]['AtRisk'] = "Yes"
                    if edge < Node:
                        AddAtRiskEdges.add(((edge,Node),Node_block))
                    else:
                        AddAtRiskEdges.add(((Node,edge),Node_block))

        # Add or remove any edges that need to be added or removed
        if len(RemoveAtRiskEdges) > 0:
            for pair in RemoveAtRiskEdges:
                AtRiskEdges[pair[1]].remove(pair[0])
        if len(AddAtRiskEdges) > 0:
            for pair in AddAtRiskEdges:
                AtRiskEdges[pair[1]].add(pair[0])

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


# UpdateBlockEdges will update the edges of the network after infection or recovery
def UpdateBlockEdges(G,SIEdges,Node,Type):
    node_block = G.nodes[Node]['block']
    # For each edge involving the Node
    for node in G[Node]:
        neighbor_block = G.nodes[node]['block']

        # Write down the edge
        if node < Node:
            edge = (node,Node)
        else:
            edge = (Node,node)

        blocks = [node_block,neighbor_block]

        # If Node recovered
        if Type == "S":
            if G.nodes[node]['Status'] == "S":
                SIEdges[neighbor_block].remove(edge)
                Update = "SS"
            elif G.nodes[node]['Status'] == "I":
                SIEdges[node_block].add(edge)
                Update = "SI"

        # If Node got infected
        elif Type == "I":
            if G.nodes[node]['Status'] == "S":
                SIEdges[neighbor_block].add(edge)
                Update = "SI"
            elif G.nodes[node]['Status'] == "I":
                SIEdges[node_block].remove(edge)
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

# Will randomly infect a node within the selected Partitions, only
# for use when G is block model.
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

# Recover function for Block Model
def BlockRecover(G,Infected):
    node = random.sample(Infected,1)[0]
    Infected.remove(node)
    G.nodes[node]['Status'] = "S"
    PartitionEvent = "Partition" + str(G.node[node]['block']) + "_Recovery"
    return node,G,Infected,PartitionEvent

# Given a set of SI edges this randomly selects one and th
def Infect(G,Infected,SIEdges):
    edge = random.sample(SIEdges,1)[0]
    for item in edge:
        if G.nodes[item]['Status'] == "S":
            node = item
            Infected.add(item)

    G.nodes[node]['Status'] = "I"
    return node,G,Infected

# Infect function for block model graphs
def BlockInfect(G,Infected,SIEdges):
    edge = random.sample(SIEdges,1)[0]

    for item in edge:
        if G.nodes[item]['Status'] == "S":
            node = item
            Infected.add(item)

    G.nodes[node]['Status'] = "I"
    PartitionEvent = "Partition" + str(G.node[node]['block']) + "_Infection"
    return node,G,Infected,PartitionEvent


# Will calculate the overall reaction rate
def CalculateRate(SIEdges,Infected,beta,gamma):
    rate = beta*len(SIEdges) + gamma*len(Infected)
    return rate

# This will calculate the reaction rate for a block model simulation,
# we assume that gamma is constant along the entire network
def CalculateBlockRate(EdgeList,Infected,betas,gamma):
    rate = gamma*len(Infected)
    for i in range(len(EdgeList)):
        rate = rate + betas[i]*len(EdgeList[i])
    return rate

# This function decides if an infection or recovery happened
def WhatHappened(Infected,rate,gamma):
    u = random.uniform(0,rate)
    if u < gamma*len(Infected):
        event = "Recovery"
    else:
        event = "Infection"

    return event

# WhatHappened function fo block model, we assume that gamma is constant
# for all nodes.
def BlockWhatHappened(EdgeList,Infected,rate,betas,gamma):
    u = random.uniform(0,rate)
    upper_bound = gamma*len(Infected)
    lower_bound = gamma*len(Infected)
    if u < gamma*len(Infected):
        event = "Recovery"
        block = "Null"
    else:
        event = "Infection"
        for i in range(len(betas)):
            lower_bound = upper_bound
            upper_bound = upper_bound + betas[i]*len(EdgeList[i])
            if lower_bound <= u < upper_bound:
                block = i

    return event,block

# Simulation of simple contagion over a network
def SimpleSim(G,InitialFrac,StoppingTime,gamma,beta):
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

# Simulation for complex contagion over
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

    return Time,Events,CurrentInfected

# Simple Contagion Simulation function for block Model
# Note this might need to be updated.
def SimpleBlockSim(G,InitialFrac,WhereInfect,StoppingTime,gamma,beta):
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
    PartitionEvents = ["Start"]
    rate = 1

    while (CurrentTime < StoppingTime) & (len(Infected) > 0) & (rate > 0):
        # Find the time until the next event
        rate = CalculateRate(SIEdges,Infected,beta,gamma)
        WaitingTime = random.expovariate(rate)
        WaitingTimes.append(WaitingTime)

        Event = WhatHappened(Infected,rate,gamma)
        Events.append(Event)


        if Event == "Recovery":
            ChangedNode,G,Infected,PartitionEvent = BlockRecover(G,Infected)
            Type = "S"
        elif Event == "Infection":
            ChangedNode,G,Infected,PartitionEvent = BlockInfect(G,Infected,SIEdges)
            Type = "I"

        PartitionEvents.append(PartitionEvent)

        G,SIEdges = UpdateEdges(G,SIEdges,ChangedNode,Type)

        CurrentTime = CurrentTime + WaitingTime

        Time.append(CurrentTime)
        CurrentInfected.append(len(Infected))
        for i in range(NPartitions):
            PartitionInfected[i].append(len(Infected.intersection(G.graph['partition'][i])))


    return Time,Events,CurrentInfected,PartitionInfected,PartitionEvents

# Complex Contagion Simulation for a block model graph.
def ComplexBlockSim(G,InitialFrac,WhereInfect,StoppingTime,gamma,betas,Thresholds,ThresholdType):
    # Set all the nodes to susceptible
    nx.set_node_attributes(G,"S",'Status')

    # Get a set of the subgraphs
    subgraphs = [[G.subgraph([node for node in G.nodes if G.nodes[node]['block'] == i]),i] for i in range(len(G.graph['partition']))]


    # Set all the nodes threshold
    for graph in subgraphs:
        nx.set_node_attributes(graph[0],Thresholds[graph[1]],'Threshold')

    # Set all the edges to SS
    nx.set_edge_attributes(G,"SS",'Type')

    # Set all edges to not at risk
    nx.set_edge_attributes(G,"No",'AtRisk')


    Infected = set([])
    SIEdges = []
    AtRiskEdges = []

    for graph in subgraphs:
        SIEdges.append(set([]))
        AtRiskEdges.append(set([]))

    InfectSeed = int(InitialFrac * len(G.nodes))

    Partitions = []
    for i in WhereInfect:
        Partitions.append(G.graph['partition'][i])

    for i in range(InfectSeed):
        node,G,Infected = InitialBlockInfect(G,Partitions,Infected)
        G,SIEdges = UpdateBlockEdges(G,SIEdges,node,"I")\
        G,AtRiskEdges = UpdateBlockAtRisk(G,AtRiskEdges,node,"I",ThresholdType)

    del Partitions

    NPartitions = len(subgraphs)

    PartitionInfected = []

    for i in range(NPartitions):
        PartitionInfected.append([])
        PartitionInfected[i].append(len(Infected.intersection(G.graph['partition'][i])))

    CurrentTime = 0
    Time = [CurrentTime]
    CurrentInfected = [len(Infected)]

    WaitingTimes = []
    Events = ["Start"]
    PartitionEvents = ["Start"]
    rate = 1

    while (CurrentTime < StoppingTime) & (len(Infected) > 0):
        rate = CalculateBlockRate(AtRiskEdges,Infected,betas,gamma)
        WaitingTime = random.expovariate(rate)
        WaitingTimes.append(WaitingTime)

        Event,block = BlockWhatHappened(AtRiskEdges,Infected,rate,betas,gamma)
        Events.append(Event)

        if Event == "Recovery":
            ChangedNode,G,Infected,PartitionEvent = BlockRecover(G,Infected)
            Type = "S"
        elif Event == "Infection":
            ChangedNode,G,Infected,PartitionEvent = BlockInfect(G,Infected,AtRiskEdges[block])
            Type = "I"

        PartitionEvents.append(PartitionEvent)

        G,SIEdges = UpdateBlockEdges(G,SIEdges,ChangedNode,Type)
        G,AtRiskEdges = UpdateBlockAtRisk(G,AtRiskEdges,ChangedNode,Type,ThresholdType)

        CurrentTime = CurrentTime + WaitingTime

        Time.append(CurrentTime)
        CurrentInfected.append(len(Infected))

        for i in range(NPartitions):
            PartitionInfected[i].append(len(Infected.intersection(G.graph['partition'][i])))

    return Time,Events,CurrentInfected,PartitionInfected,PartitionEvents
