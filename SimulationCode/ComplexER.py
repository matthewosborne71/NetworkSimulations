import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440

Nodes = [1000]
EdgeProbs = [.25,.3,.4,.5]
betas = [1.5]
Thresholds = np.arange(0.0025,0.0525,0.0025)

gamma = 1

NumSims = 30

InitialFrac = 0.01

StoppingTime = 3

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/ComplexSimER2.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_ER.csv","a")
#f.write("Nodes,EdgeProb,beta,Threshold,SimNum,EventTime,Event,CurrentI\n")

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