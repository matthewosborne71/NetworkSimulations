import CreateNetworks as CN
import Simulation as S
import numpy as np
import logging
import Path

seed = 440

InitialFrac = .01
StoppingTime = 5
gamma = 1
First = True

# k = 40
#Networks = ['Haverford76','Hamilton46','Amherst41','Williams40']

# k = 20
Networks = ['Caltech36','Reed98','Simmons81']


betas = [1.5]
Thresholds = [.05,.1,.15,.2]
NumSims = 50

path = Path.GetPath()


logging.basicConfig(filename = path + "Logs/ComplexSimFB100.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_FB100.csv","w+")
f.write("Network,beta,Threshold,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(Networks) * len(betas) * len (Thresholds) * NumSims
CurrentSim = float(1)

logging.info("About to run Complex Contagion Simulations on the FB100 Networks.\r\n")

for Network in Networks:
    Edgelist = path + "Code/" + Network + "_Edgelist.csv"
    for thresh in Thresholds:
        for beta in betas:
            for i in range(1,NumSims+1):
                logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
                CurrentSim = CurrentSim + 1

                G = CN.Facebook100(Edgelist)

                Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,thresh,"Frac")

                for j in range(len(Times)):
                    Threshold = str(thresh)
                    Beta = str(beta)
                    SimNum = str(i)
                    EventTime = str(Times[j])
                    Event = str(Events[j])
                    CurrentI = str(Is[j])
                    f.write(Network + "," + Beta + "," + Threshold + "," +
                            SimNum + "," + EventTime + "," + Event + "," +
                            CurrentI + "\n")

f.close()

logging.info("All Done! :-D")
