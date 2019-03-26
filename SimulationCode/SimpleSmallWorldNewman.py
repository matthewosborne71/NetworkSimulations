import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path
import math

seed = 440

Nodes = 1000
k = 6

ps = np.arange(.1,1.1,.1)

gamma = 1

betas = [1.5]


NumSims = 50
InitialFrac = 0.01
StoppingTime = 10

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/SimpleSimSmallNewman.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/SimpleComparison_SmallWorldNewman.csv","w+")
#f = open(path + "SimpleContagionSimulations_SmallWorld.csv","w+")
f.write("Nodes,k,ShortCutProb,beta,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(ps) * len(betas) * NumSims
CurrentSim = float(1)

logging.info("About to run the simulations for the Simple Contagion Small World Newman Network.\r\n")

for p in ps:
    m = math.ceil(float(k)/(1+p))
    for beta in betas:
        for i in range(1,NumSims+1):
            logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
            CurrentSim = CurrentSim + 1
            if First:
                G = CN.SmallWorldNewman(Nodes,m,p,seed)
                First = False
            else:
                G = CN.SmallWorldNewman(Nodes,m,p)

            Times,Events,Is = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)

            for j in range(len(Times)):
                nodes = str(Nodes)
                K = str(int(m))
                ShortCutProb = str(p)
                Beta = str(beta)
                SimNum = str(i)
                EventTime = str(Times[j])
                Event = str(Events[j])
                CurrentI = str(Is[j])
                f.write(nodes + "," + K + "," + ShortCutProb + "," + Beta + ","
                        + SimNum + "," + EventTime + "," + Event + "," +
                        CurrentI + "\n")

f.close()

logging.info("All Done! :-)")
