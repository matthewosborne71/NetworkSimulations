import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440
np.random.seed(seed)

Nodes = 1000
probs = [.5]
num_successes = [10]
Thresholds = np.arange(0.05,0.55,0.05)

gamma = 1
beta = 1.5

NumSims = 50
InitialFrac = 0.01
StoppingTime = 5

path = Path.GetPath()

logging.basicConfig(filename = path + "Logs/ComplexSimNegativeBinomial.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_NegativeBinomial.csv","w+")
f.write("Nodes,Prob,Num_Success,beta,Threshold,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(probs) * len(num_successes) * len(Thresholds) * NumSims
CurrentSim = float(1)

for p in probs:
    for n in num_successes:
        for thresh in Thresholds:
            for i in range(1,NumSims+1):
                logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
                CurrentSim = CurrentSim + 1
                G = CN.NegativeBinomial(Nodes,p,n)

                Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,thresh,"Frac")

                for j in range(len(Times)):
                    nodes = str(Nodes)
                    prob = str(p)
                    Succ = str(n)
                    Beta = str(beta)
                    threshold = str(thresh)
                    SimNum = str(i)
                    EventTime = str(Times[j])
                    Event = str(Events[j])
                    CurrentI = str(Is[j])
                    f.write(nodes + "," + prob + "," + Succ + "," + Beta + "," + threshold + "," + SimNum + "," + EventTime
                            + "," + Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-)")
