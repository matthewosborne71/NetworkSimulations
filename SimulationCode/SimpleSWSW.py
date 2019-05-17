import CreateNetworks as CN
import Simulation as S
import numpy as np
import logging
import Path

seed = 440
NumSims = 50

np.random.seed(seed)

size = 1000
k = 10
p = .3

prob = [[0,0.001],[0.001,0]]
parts = [[0],[1],[0,1]]

gamma = 1
beta = 1.5

InitialFrac = 0.005

StoppingTime = 5

path = Path.GetPath()

logging.basicConfig(filename = path + "Logs/SimpleSWSW.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/SimpleContagionSimulations_SW_SW.csv","w+")
f.write("Partition,SimNum,EventTime,Event,PartitionEvent,CurrentI,")
for i in range(len(prob)):
    if i < len(prob) - 1:
        f.write("Partition" + str(i) + "_I,")
    else:
        f.write("Partition" + str(i) + "_I\n")

TotalSims = NumSims * len(parts)

CurrentSim = float(1)

logging.info("About to run simulations for SW SW block model \n")

for part in parts:
    WhereInfect = part
    for i in range(1,NumSims + 1):
        logging.info("About to run sim " + str(CurrentSim) + " of " + str(TotalSims) + ": " + str(WhereInfect) + ".\n")
        CurrentSim = CurrentSim + 1

        Gs = [CN.SmallWorld(size,k,p),CN.SmallWorld(size,k,p)]

        G = CN.GeneralBlock(Gs,prob)
        del Gs

        Times,Events,Is,PartIs,PartitionEvents = S.SimpleBlockSim(G,InitialFrac,WhereInfect,StoppingTime,gamma,beta)

        for j in range(len(Times)):
            Part = '"' + str(part) + '"'
            SimNum = str(i)
            EventTime = str(Times[j])
            Event = str(Events[j])
            CurrentI = str(Is[j])
            PEvent = str(PartitionEvents[j])
            f.write(Part + "," + SimNum + "," + EventTime + "," + Event + "," + PEvent + "," + CurrentI + ",")
            for m in range(len(prob)):
                if m < len(prob) - 1:
                    f.write(str(PartIs[m][j]) + ",")
                else:
                    f.write(str(PartIs[m][j]) + "\n")


f.close()
logging.info("All Done! :-)")
