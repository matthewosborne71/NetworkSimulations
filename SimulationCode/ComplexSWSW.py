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

prob = [[0,.001],[.001,0]]
parts = [[0],[1],[0,1]]

Thresholds = [.02,.04,.06,.08,.1,.12,.14,.16,.18,.2]

gamma = 1
beta = 1.5

InitialFrac = 0.005

StoppingTime = 5

path = Path.GetPath()

logging.basicConfig(filename = path + "Logs/ComplexSWSW.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_SW_SW.csv","w+")
f.write("Partition,Threshold,SimNum,EventTime,Event,PartitionEvent,CurrentI,")
for i in range(len(prob)):
    if i < len(prob) - 1:
        f.write("Partition" + str(i) + "_I,")
    else:
        f.write("Partition" + str(i) + "_I\n")

TotalSims = NumSims * len(parts) * len(Thresholds)

CurrentSim = float(1)

logging.info("About to run simulations for the SW SW block model \n")

for thresh in Thresholds:
    for part in parts:
        WhereInfect = part
        for i in range(1,NumSims + 1):
            logging.info("About to run sim " + str(CurrentSim) + " of " + str(TotalSims) +".\n")
            CurrentSim = CurrentSim + 1

            Gs = [CN.SmallWorld(size,k,p),CN.SmallWorld(size,k,p)]
            G = CN.GeneralBlock(Gs,prob)


            Times,Events,Is,PartIs,PartitionEvents = S.ComplexBlockSim(G,InitialFrac,WhereInfect,StoppingTime,gamma,beta,thresh,"Frac")

            for j in range(len(Times)):
                Threshold = str(thresh)
                Part = '"' + str(part) + '"'
                SimNum = str(i)
                EventTime = str(Times[j])
                Event = str(Events[j])
                PEvent = str(PartitionEvents[j])
                CurrentI = str(Is[j])
                f.write(Part + "," + Threshold + "," + SimNum +
                        "," + EventTime + "," + Event + "," + PEvent + "," +
                        CurrentI + ",")
                for m in range(len(prob)):
                    if m < len(prob) - 1:
                        f.write(str(PartIs[m][j]) + ",")
                    else:
                        f.write(str(PartIs[m][j]) + "\n")

f.close()
logging.info("Nice one! B)")
