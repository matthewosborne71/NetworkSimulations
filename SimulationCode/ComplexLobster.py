import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440

Nodes = 1000
p1s = np.arange(.6,1.1,.1)
p2s = np.arange(.6,1.1,.1)

Thresholds = np.arange(0.05,0.4,0.05)

betas = [1.5]
gamma = 1

NumSims = 50
InitialFrac = 0.01
StoppingTime = 2

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/ComplexSimLobster.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_Lobster.csv","w+")

f.write("Nodes,p1,p2,Threshold,beta,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(betas) * len(p1s) * len(p2s) * NumSims * len(Thresholds)
CurrentSim = float(1)

logging.info("Running Simple Sims on Random Lobster.")

for p1 in p1s:
    for p2 in p2s:
        for Threshold in Thresholds:
            for beta in betas:
                for i in range(1,NumSims+1):
                    logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
                    CurrentSim = CurrentSim + 1
                    if First:
                        G = CN.RandomLobster(Nodes,p1,p2,seed)
                        First = False
                    else:
                        G = CN.RandomLobster(Nodes,p1,p2)

                    Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,Threshold,"Frac")

                    for j in range(len(Times)):
                        nodes = str(Nodes)
                        P1 = str(p1)
                        P2 = str(p2)
                        Beta = str(beta)
                        SimNum = str(i)
                        Thresh = str(Threshold)
                        EventTime = str(Times[j])
                        Event = str(Events[j])
                        CurrentI = str(Is[j])
                        f.write(nodes + "," + P1 + "," + P2 + "," + Thresh + ","
                                + Beta + "," + SimNum + "," + EventTime + "," +
                                Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-D")
