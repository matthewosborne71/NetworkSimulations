import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path



path = Path.GetPath()

logging.basicConfig(filename = path + "Logs/ComparisonNonRandom.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

# For 1-D
Nodes = 1000
k = 6
p = 0

# For Triangular Lattice
Ns = [200,100,50]
Ms = [9,19,38]
periodic = True

# For 3-D Grid
Dims = [[10,10,10],[20,5,10],[25,8,5]]

beta = 1.5
gamma = 1

NumSims = 50
InitialFrac = 0.01
StoppingTime = 10


Thresholds = [0, float(1)/float(6), float(2)/float(6), float(3)/float(6),
                float(4)/float(6)]

TotalSims = NumSims * (1 + len(Ns) + len(Dims)) * len(Thresholds)
CurrentSim = float(1)


f = open(path + "SimulationResults/ComparisonNonRandom.csv","w+")
f.write("NetworkType,FeatureStat,Threshold,SimNum,EventTime,Event,CurrentI\n")

logging.info("About to Run Sims for the 1-D Lattice Network.")
Feature = "'[6]'"
NetworkType = "1DLattice"
for Threshold in Thresholds:
    Thresh = str(Threshold)
    for i in range(1,NumSims + 1):
        logging.info("Currently at " + str(100*CurrentSim/float(TotalSims))  + "% of the Simulations Done.\n")
        CurrentSim = CurrentSim + 1

        G = CN.SmallWorld(Nodes,k,p)

        if Threshold == 0:
            Times,Events,Is = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)
        else:
            Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,Threshold,"Frac")

        for j in range(len(Times)):
            SimNum = str(i)
            EventTime = str(Times[j])
            Event = str(Events[j])
            CurrentI = str(Is[j])
            f.write(NetworkType + "," + Feature + "," + Thresh + "," + SimNum +
                    "," + EventTime + "," + Event + "," + CurrentI + "\n")

logging.info("About to run sims for the Triangular Lattice Network.")
NetworkType = "TriangularLattice"
for Threshold in Thresholds:
    Thresh = str(Threshold)
    for k in range(len(Ns)):
        Feature = "'[" + str(Ms[k]) + "," + str(Ns[k]) + "]'"
        for i in range(1,NumSims + 1):
            logging.info("Currently at " + str(100*CurrentSim/float(TotalSims))  + "% of the Simulations Done.\n")
            CurrentSim = CurrentSim + 1

            G = CN.TriangularGridGraph(Ms[k],Ns[k],periodic)

            if Threshold == 0:
                Times,Events,Is = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)
            else:
                Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,Threshold,"Frac")

            for j in range(len(Times)):
                SimNum = str(i)
                EventTime = str(Times[j])
                Event = str(Events[j])
                CurrentI = str(Is[j])
                f.write(NetworkType + "," + Feature + "," + Thresh + "," + SimNum +
                        "," + EventTime + "," + Event + "," + CurrentI + "\n")

logging.info("About to run sims for the 3-D Lattice.")
NetworkType = "3DLattice"
for Threshold in Thresholds:
    Thresh = str(Threshold)
    for k in range(len(Dims)):
        Feature = "'" + str(Dims[k]) + "'"
        for i in range(1,NumSims + 1):
            logging.info("Currently at " + str(100*CurrentSim/float(TotalSims))  + "% of the Simulations Done.\n")
            CurrentSim = CurrentSim + 1

            G = CN.GridGraph(Dims[k],periodic)

            if Threshold == 0:
                Times,Events,Is = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)
            else:
                Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,Threshold,"Frac")

            for j in range(len(Times)):
                SimNum = str(i)
                EventTime = str(Times[j])
                Event = str(Events[j])
                CurrentI = str(Is[j])
                f.write(NetworkType + "," + Feature + "," + Thresh + "," + SimNum +
                        "," + EventTime + "," + Event + "," + CurrentI + "\n")

f.close()

logging.info("All Done! :-)")
