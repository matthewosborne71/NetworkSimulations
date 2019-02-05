import CreateNetworks as CN
import Simulation as S
import logging
import Path

seed = 440

InitialFrac = .01
StoppingTime = 7
gamma = 1
First = True


betas = [1.5]
NumSims = 50

path = Path.GetPath()


logging.basicConfig(filename = path + "Logs/SimpleSimFacebook.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

f = open(path + "SimulationResults/SimpleContagionSimulations_Facebook.csv","w+")
f.write("beta,SimNum,EventTime,Event,CurrentI\n")

TotalSims = len(betas) * NumSims
CurrentSim = float(1)

logging.info("About to run Simple Contagion Simulations on the Facebook Network.\r\n")



for beta in betas:
    for i in range(1,NumSims+1):
        logging.info("Currently at " + str(100*CurrentSim/float(TotalSims)) + "% of the Simulations Done.\n")
        CurrentSim = CurrentSim + 1

        G = CN.SNAPFacebook()

        Times,Events,Is = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)

        for j in range(len(Times)):
            Beta = str(beta)
            SimNum = str(i)
            EventTime = str(Times[j])
            Event = str(Events[j])
            CurrentI = str(Is[j])
            f.write(Beta + "," + SimNum + "," + EventTime + "," + Event + "," +
                    CurrentI + "\n")

f.close()

logging.info("All Done! :-D")
