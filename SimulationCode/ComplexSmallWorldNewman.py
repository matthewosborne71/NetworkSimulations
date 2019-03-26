import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import math
import Path

seed = 440

Nodes = 1000
k = 10

ps = np.arange(.1,1.1,.1)

gamma = 1

betas = [1.5]

Thresholds = Thresholds = [0, float(1)/float(6), float(2)/float(6), float(3)/float(6),
                float(4)/float(6)]


NumSims = 50
InitialFrac = 0.01
StoppingTime = 10

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/ComplexSimSmallNewman.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexComparison_SmallWorldNewman.csv","w+")
#f = open(path + "ComplexContagionSimulations_SmallWorld.csv","w+")
f.write("Nodes,k,ShortCutProb,beta,Threshold,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(ps) * len(betas) * len(Thresholds) * NumSims
CurrentSim = float(1)

logging.info("About to run the simulations for the Simple Contagion Small World Newman Network.\r\n")

for thresh in Thresholds:
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

                Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,thresh,"Frac")

                for j in range(len(Times)):
                    threshold = str(thresh)
                    nodes = str(Nodes)
                    K = str(int(m))
                    ShortCutProb = str(p)
                    Beta = str(beta)
                    SimNum = str(i)
                    EventTime = str(Times[j])
                    Event = str(Events[j])
                    CurrentI = str(Is[j])
                    f.write(nodes + "," + K + "," + ShortCutProb + "," + Beta + ","
                            + threshold + "," + SimNum + "," + EventTime + "," +
                            Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-)")
