import CreateNetworks as CN
import Simulation as S
import numpy as np
import logging
import Path

seed = 440

InitialFrac = .01
StoppingTime = 10
gamma = 1
First = True


betas = [1.5]
Thresholds = [.01,.02,.03,.04,.05,.06,.07]
NumSims = 50

path = Path.GetPath()


logging.basicConfig(filename = path + "Logs/ComplexSimFacebook.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_Facebook.csv","w+")
f.write("beta,Threshold,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(betas) * len (Thresholds) * NumSims
CurrentSim = float(1)

logging.info("About to run Complex Contagion Simulations on the Facebook Network.\r\n")


for thresh in Thresholds:
    for beta in betas:
        for i in range(1,NumSims+1):
            logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
            CurrentSim = CurrentSim + 1

            G = CN.SNAPFacebook()

            Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,thresh,"Frac")

            for j in range(len(Times)):
                Threshold = str(thresh)
                Beta = str(beta)
                SimNum = str(i)
                EventTime = str(Times[j])
                Event = str(Events[j])
                CurrentI = str(Is[j])
                f.write(Beta + "," + Threshold + "," + SimNum + "," + EventTime
                        + "," + Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-D")
