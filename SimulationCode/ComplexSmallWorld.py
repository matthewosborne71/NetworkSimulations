import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440

Nodes = 1000
k = 40

ps = np.arange(0,1.05,.05)

gamma = 1

betas = [1.5]

Thresholds = np.arange(0.01,.12,.01)


NumSims = 50
InitialFrac = 0.01
StoppingTime = 10

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/ComplexSimSmall.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_SmallWorld.csv","w+")
#f = open(path + "ComplexContagionSimulations_SmallWorld.csv","w+")
f.write("Nodes,k,RewiringProb,beta,Threshold,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(ps) * len(betas) * len(Thresholds) * NumSims
CurrentSim = float(1)

logging.info("About to run the simulations for the Simple Contagion Small World Network.\r\n")

for thresh in Thresholds:
    for p in ps:
        for beta in betas:
            for i in range(1,NumSims+1):
                logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
                CurrentSim = CurrentSim + 1
                if First:
                    G = CN.SmallWorld(Nodes,k,p,seed)
                    First = False
                else:
                    G = CN.SmallWorld(Nodes,k,p)

                Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,thresh,"Frac")

                for j in range(len(Times)):
                    threshold = str(thresh)
                    nodes = str(Nodes)
                    K = str(k)
                    RewiringProb = str(p)
                    Beta = str(beta)
                    SimNum = str(i)
                    EventTime = str(Times[j])
                    Event = str(Events[j])
                    CurrentI = str(Is[j])
                    f.write(nodes + "," + K + "," + RewiringProb + "," + Beta + ","
                            + threshold + "," + SimNum + "," + EventTime + "," +
                            Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-)")
