import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440
np.random.seed(seed)

Nodes = 1000

# k = 2
#probs = [.5,.6,.75,.8]
#num_successes = [2,3,6,8]

# k = 6
#probs = [.25,.4,.5,.6]
#num_successes = [2,4,6,9]

# k = 40
probs = [.33333,.5,.6]
num_successes = [20,40,60]

gamma = 1
beta = 1.5

NumSims = 50
InitialFrac = 0.01
StoppingTime = 5

path = Path.GetPath()

logging.basicConfig(filename = path + "Logs/SimpleSimNegativeBinomial.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/SimpleComparison_NegativeBinomial.csv","w+")
f.write("Nodes,Prob,Num_Success,beta,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(probs) * NumSims
CurrentSim = float(1)

for m in range(len(probs)):
    p = probs[m]
    n = num_successes[m]
    for i in range(1,NumSims+1):
        logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
        CurrentSim = CurrentSim + 1
        G = CN.NegativeBinomial(Nodes,p,n)

        Times,Events,Is = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)

        for j in range(len(Times)):
            nodes = str(Nodes)
            prob = str(p)
            Succ = str(n)
            Beta = str(beta)
            SimNum = str(i)
            EventTime = str(Times[j])
            Event = str(Events[j])
            CurrentI = str(Is[j])
            f.write(nodes + "," + prob + "," + Succ + "," + Beta + "," + SimNum + "," + EventTime
                    + "," + Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-)")
