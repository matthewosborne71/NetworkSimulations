import CreateNetworks as CN
import Simulation as S
import logging
import Path

seed = 440
NumSims = 100

sizes = [500,500]
probs = [[0.1,0.001],[0.001,0.005]]

gamma = 1
beta = 0.2

InitialFrac = 0.01

StoppingTime = 5

WhereInfect = [1]

path = Path.GetPath()

First = True

logging.basicConfig(filename = path + "Logs/BlockSims.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/Simulations_BlockModel_Infect1.csv","w+")
f.write("SimNum,EventTime,Event,CurrentI,")
for i in range(len(sizes)):
    if i < len(sizes) - 1:
        f.write("Partition" + str(i) + "_I,")
    else:
        f.write("Partition" + str(i) + "_I\n")

TotalSims = NumSims

CurrentSim = float(1)

logging.info("About to run simulations for The block model\n")

for i in range(1,NumSims + 1):
    logging.info("About to run sim " + str(CurrentSim) + " of " + str(TotalSims) +".\n")
    CurrentSim = CurrentSim + 1

    if First:
        First = False
        G = CN.Block(sizes,probs,seed)
    else:
        G = CN.Block(sizes,probs)


    Times,Events,Is,PartIs = S.SimpleBlockSim(G,InitialFrac,WhereInfect,StoppingTime,gamma,beta)

    for j in range(len(Times)):
        SimNum = str(i)
        EventTime = str(Times[j])
        Event = str(Events[j])
        CurrentI = str(Is[j])
        f.write(SimNum + "," + EventTime + "," + Event + "," + CurrentI + ",")
        for k in range(len(sizes)):
            if k < len(sizes) - 1:
                f.write(str(PartIs[k][j]) + ",")
            else:
                f.write(str(PartIs[k][j]) + "\n")

f.close()
logging.info("All Done! :-)")
