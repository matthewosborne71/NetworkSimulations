import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440
np.random.seed(seed)

Nodes = 1000

# k = 2
exps = [2.478]

# k = 6
# exps = [2.1145]

gamma = 1
beta = 1.5

NumSims = 50
InitialFrac = 0.01
StoppingTime = 20


path = Path.GetPath()

logging.basicConfig(filename = path + "Logs/SimpleSimPowerLaw.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/SimpleComparison_PowerLaw.csv","w+")
f.write("Nodes,exponent,beta,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(exps)*NumSims
CurrentSim = float(1)

for e in exps:
    for i in range(1,NumSims):
        logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
        CurrentSim = CurrentSim + 1
        G = CN.PowerLaw(Nodes,e)

        Times,Events,Is = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)

        for j in range(len(Times)):
            nodes = str(Nodes)
            Exp = str(e)
            Beta = str(beta)
            SimNum = str(i)
            EventTime = str(Times[j])
            Event = str(Events[j])
            CurrentI = str(Is[j])
            f.write(nodes + "," + Exp + "," + Beta + "," + SimNum + "," + EventTime
                    + "," + Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-)")
