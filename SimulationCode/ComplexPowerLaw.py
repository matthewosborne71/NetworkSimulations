import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

Nodes = 1000

# k = 2
exps = [2.478]

# k = 6
# exps = [2.1145]

gamma = 1
beta = 1.5

Thresholds = [.05,.1,.15,.2]

NumSims = 50
InitialFrac = 0.01
StoppingTime = 20

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/ComplexSimPowerLaw.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexComparison_PowerLaw.csv","w+")
f.write("Nodes,exponent,beta,Threshold,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(exps)*len(Thresholds)*NumSims
CurrentSim = float(1)

logging.info("About to run simulations for complex contagion power law\n")

for e in exps:
    for thresh in Thresholds:
        for i in range(1,NumSims+1):
            logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
            CurrentSim = CurrentSim + 1

            G = CN.PowerLaw(Nodes,e)

            Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,thresh,"Frac")

            for j in range(len(Times)):
                threshold = str(thresh)
                nodes = str(Nodes)
                Exp = str(e)
                Beta = str(beta)
                SimNum = str(i)
                EventTime = str(Times[j])
                Event = str(Events[j])
                CurrentI = str(Is[j])
                f.write(nodes + "," + Exp + "," + Beta + "," + threshold + "," +
                        SimNum + "," + EventTime + "," + Event + "," + CurrentI +
                        "\n")

f.close()

logging.info("All Done! :-)")
