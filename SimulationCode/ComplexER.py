import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440

Nodes = [1000]

# k = 2
# EdgeProbs = [0.002]

# k = 6
# EdgeProbs = [0.006]

# k = 40
#EdgeProbs = [0.04]

# k = 20
EdgeProbs = [0.02]

betas = [1.5]
Thresholds = [.05,.1,.15,.2]

gamma = 1

NumSims = 50

InitialFrac = 0.01

StoppingTime = 5

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/ComplexSimER.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexComparison_ER.csv","w+")
f.write("Nodes,EdgeProb,beta,Threshold,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(Nodes) * len(EdgeProbs) * len(betas) * len(Thresholds) * NumSims
CurrentSim = float(1)

logging.info("About to run the simulations for the Complex Contagion ER Network.\r\n")

for node in Nodes:
    for prob in EdgeProbs:
        for beta in betas:
            for threshold in Thresholds:
                for i in range(1,NumSims + 1):
                    logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
                    CurrentSim = CurrentSim + 1

                    if First:
                        G = CN.Erdos(node,prob,seed)
                        First = False
                    else:
                        G = CN.Erdos(node,prob)

                    Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,threshold,"Frac")

                    for j in range(len(Times)):
                        nodes = str(node)
                        EdgeProb = str(prob)
                        Beta = str(beta)
                        SimNum = str(i)
                        EventTime = str(Times[j])
                        Event = str(Events[j])
                        CurrentI = str(Is[j])
                        Threshold = str(threshold)
                        f.write(nodes + "," + EdgeProb + "," + Beta + "," +
                                Threshold + "," + SimNum + "," + EventTime
                                 + "," + Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-)")
