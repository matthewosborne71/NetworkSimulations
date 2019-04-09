import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440

Nodes = 1000

# k = 2
ms = [1]

# k = 6
# ms = [3]

Thresholds = [.05,.1,.15,.2]

betas = [1.5]
gamma = 1

NumSims = 50
InitialFrac = 0.01
StoppingTime = 20

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/ComplexSimBA.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexComparison_BA.csv","w+")

f.write("Nodes,m,Threshold,beta,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(Thresholds) * len(betas) * NumSims * len(ms)
CurrentSim = float(1)

for m in ms:
    for Threshold in Thresholds:
        for beta in betas:
            for i in range(1,NumSims+1):
                logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
                CurrentSim = CurrentSim + 1
                if First:
                    G = CN.BarabasiAlbert(Nodes,m,seed)
                    First = False
                else:
                    G = CN.BarabasiAlbert(Nodes,m)

                Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,Threshold,"Frac")

                for j in range(len(Times)):
                    nodes = str(Nodes)
                    M = str(m)
                    Thresh = str(Threshold)
                    Beta = str(beta)
                    SimNum = str(i)
                    EventTime = str(Times[j])
                    Event = str(Events[j])
                    CurrentI = str(Is[j])
                    f.write(nodes + "," + M + "," + Thresh + "," + Beta + "," +
                            SimNum + "," + EventTime + "," + Event + "," + CurrentI
                            + "\n")

f.close()

logging.info("All Done! :-D")
