import CreateNetworks as CN
import Simulation as S
import logging
import numpy as np
import Path

Ns = [50,100,200]
Ms = [40,20,10]
Periodic = [True,False]

Thresholds = np.arange(0.1,0.5 + float(1)/float(6),float(1)/float(6))
betas = [1.5]
gamma = 1

NumSims = 50
InitialFrac = 0.01
StoppingTime = 20

path = Path.GetPath()

logging.basicConfig(filename = path + "Logs/ComplexSimGrid.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/ComplexContagionSimulations_Lattice.csv","w+")

f.write("N,M,Periodic,Threshold,beta,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(Ns) * len(Periodic) * len(betas) * len(Thresholds) * NumSims
CurrentSim = float(1)

logging.info("About to run simple sims for Triangular Lattice.")

for P in Periodic:
    for k in range(len(Ns)):
        for beta in betas:
            for Thresh in Thresholds:
                for i in range(1,NumSims+1):
                    logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
                    CurrentSim = CurrentSim + 1

                    G = CN.TriangularGridGraph(Ns[k],Ms[k],P)

                    Times,Events,Is = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,Thresh,"Frac")

                    for j in range(len(Times)):
                        n = str(Ns[k])
                        m = str(Ms[k])
                        p = str(P)
                        Beta = str(beta)
                        SimNum = str(i)
                        EventTime = str(Times[j])
                        Event = str(Events[j])
                        CurrentI = str(Is[j])
                        Threshold = str(Thresh)
                        f.write(n + "," + m + "," + p + "," + Threshold + "," +
                                Beta + "," + SimNum + "," + EventTime + "," +
                                Event + "," + CurrentI + "\n")


f.close()

logging.info("All Done! :-D")
