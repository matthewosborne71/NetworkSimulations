import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440

Nodes = 1000
d = 6

betas = [1.5]
gamma = 1

NumSims = 50
InitialFrac = 0.01
StoppingTime = 2

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/SimpleSimRandomRegular.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/SimpleComparison_RandomRegular.csv","w+")

f.write("Nodes,d,beta,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(betas) * NumSims
CurrentSim = float(1)

logging.info("About to run Simple Sims for Random Regular network.")

for beta in betas:
    for i in range(1,NumSims+1):
        logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
        CurrentSim = CurrentSim + 1
        if First:
            G = CN.RandomRegularGraph(d,Nodes,seed)
            First = False
        else:
            G = CN.RandomRegularGraph(d,Nodes)

        Times,Events,Is = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)

        for j in range(len(Times)):
            nodes = str(Nodes)
            D = str(d)
            Beta = str(beta)
            SimNum = str(i)
            EventTime = str(Times[j])
            Event = str(Events[j])
            CurrentI = str(Is[j])
            f.write(nodes + "," + D + "," + Beta + "," + SimNum + "," + EventTime
                    + "," + Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-D")
