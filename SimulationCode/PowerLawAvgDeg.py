import CreateNetworks as CN
import pandas as pd
import numpy as np
import networkx as nx
import Path

path = Path.GetPath()
exps = np.arange(1.65,3.05,.05)
NumSims = 100

Nodes = 1000
seed = 440

f = open(path + "SimulationResults/PowerLaw_AverageDegree.csv","w+")
f.write("Exponent,SimNum,AverageDegree\n")

First = True

for e in exps:
    Exponent = str(e)
    for i in range(1,NumSims + 1):
        SimNum = str(i)
        if First:
            G = CN.PowerLaw(Nodes,e,seed)
        else:
            G = CN.PowerLaw(Nodes,e)

        AvgDeg = sum([deg[1] for deg in nx.degree(G)])/float(Nodes)

        AverageDegree = str(AvgDeg)
        f.write(Exponent + "," + SimNum + "," + AverageDegree + "\n")

f.close()
