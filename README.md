# NetworkSimulations
## By Matthew Osborne


This repository stores all of the code I have written in order to examine the behavior of incidence curves of complex contagion over various network topologies.

### What is a Complex Contagion?
A complex contagion is a contagious process (like a disease or behavior) in which a certain ammount of reinforcement or cooperation is needed in order for the contagion to spread. In our particular code we are considering a model presented by Watts in "A simple model of global cascades on random networks" in which you consider a contagion spreading on a network. In order for the contagion to spread from a contagious node to a susceptible node the susceptible node must have a fraction of contagious neighbors that is larger than a certain threshold. For example, I have five friends and a threshold of 1/2. If 2 of my friends are contagious but 3 are not it will not spread to me. However if 3 or more of my friends are contagious it will spread to me.

### How I model the spread
For a given network, I initially infect a certain fraction of the nodes. Then the disease spreads over the network using a <a href = "https://en.wikipedia.org/wiki/Gillespie_algorithm">Gilespie algorithm</a>. This is all facilitated with python's <a href = "https://networkx.github.io/">networkx package</a>.

### In this repository
The repository is split into two folders, one that contains all of the code I have used to run the simulations. The other contains code that cleans the data and creates pictures of the incidence vs the number of currently infected nodes in the network.

#### SimulationCode Folder
There are three file types.

1. Simulation.py - this file contains all of the code for running the simulations.
2. CreateNetworks.py - this file contains all of the code for creating the various networks I simulate on.
3. Simple/Complex*.py - these files are scripts for running complex or simple (threshold = 0) simulations on a * random graph.

#### PicCode Folder
This folder contains two types of files.

1. Aggregate*.py - these files will take the saved file from the simulations on a * random graph and aggregate the data for plotting purposes.
2. Make*Pics.py - these files will take the aggregated data and create a plot of number of infecteds vs incidence for the * random graph simulations.



