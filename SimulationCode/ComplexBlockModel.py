import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

seed = 440
NumSims = 50


sizes = [1000,1000,1000]
probs = [[0.01,0.001,0],[0.001,0.01,0.001],[0,0.001,0.01]]
parts = [[0],[1],[2],[0,1],[1,2],[0,2],[0,1,2]]

gamma = 1
beta = 1.5

InitialFrac = 0.005

StoppingTime = 5
Thresholds = [.05,.1,.15,.2,.25]

InitialFrac = 0.01

StoppingTime = 5

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/ComplexBlockSims.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_BlockModel3.csv","w+")
f.write("Partition,Threshold,SimNum,EventTime,Event,PartitionEvent,CurrentI,")
for i in range(len(sizes)):
    if i < len(sizes) - 1:
        f.write("Partition" + str(i) + "_I,")
    else:
        f.write("Partition" + str(i) + "_I\n")

TotalSims = NumSims * len(parts) * len(Thresholds)

CurrentSim = float(1)

logging.info("About to run complex simulations for The block model\n")

for thresh in Thresholds:
    for part in parts:
        for i in range(1,NumSims + 1):
            logging.info("About to run sim " + str(CurrentSim) + " of " + str(TotalSims) +".\n")
            CurrentSim = CurrentSim + 1

            if First:
                First = False
                G = CN.Block(sizes,probs,seed)
            else:
                G = CN.Block(sizes,probs)

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
                for k in range(len(sizes)):
                    if k < len(sizes) - 1:
                        f.write(str(PartIs[k][j]) + ",")
                    else:
                        f.write(str(PartIs[k][j]) + "\n")

f.close()
