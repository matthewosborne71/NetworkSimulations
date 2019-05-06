import CreateNetworks as CN
import Simulation as S
import numpy as np
import logging
import Path

seed = 440
NumSims = 50

np.random.seed(seed)

size = 1000
p = .1
exp = 2.065

probs = [[0,0.001],[0.001,0]]
parts = [[0],[1],[0,1]]

Thresholds = [.05,.1,.11,.12,.13,.14,.15,.16,.17]

gamma = 1
beta = 1.5

InitialFrac = 0.005

StoppingTime = 5

path = Path.GetPath()

logging.basicConfig(filename = path + "Logs/ComplexERPL.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_ER_PL.csv","w+")
f.write("Partition,SimNum,EventTime,Event,PartitionEvent,CurrentI,")
for i in range(len(probs)):
    if i < len(probs) - 1:
        f.write("Partition" + str(i) + "_I,")
    else:
        f.write("Partition" + str(i) + "_I\n")

TotalSims = NumSims * len(probs)

CurrentSim = float(1)

logging.info("About to run simulations for the general block model \n")

for thresh in Thresholds:
    for part in parts:
        for i in range(1,NumSims + 1):
            logging.info("About to run sim " + str(CurrentSim) + " of " + str(TotalSims) +".\n")
            CurrentSim = CurrentSim + 1

            Gs = [CN.Erdos(size,p),CN.PowerLaw(size,exp)]
            G = CN.GeneralBlock(Gs,probs)

            WhereInfect = part

            Times,Events,Is,PartIs,PartitionEvents = S.ComplexBlockSim(G,InitialFrac,WhereInfect,StoppingTime,gamma,beta,thresh,"Frac")

            for j in range(len(Times)):
                Threshold = str(thresh)
                Part = '"' + str(part) + '"'
                SimNum = str(i)
                EventTime = str(Times[j])
                Event = str(Events[j])
                PEvent = str(PartitionEvents[j])
                CurrentI = str(Is[j])
                f.write(Part + "," + Threshold + "," + SimNum + "," + EventTime
                        + "," + Event + "," + PEvent + "," + CurrentI + ",")
                for k in range(len(probs)):
                    if k < len(probs) - 1:
                        f.write(str(PartIs[k][j]) + ",")
                    else:
                        f.write(str(PartIs[k][j]) + "\n")

f.close()
