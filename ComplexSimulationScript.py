import CreateNetworks as CN
import Simulation as S


n = 1000
k = 5
p = .3

InitialFrac = .2
StoppingTime = .1
gamma =50
beta = 1
Threshold = .2
ThresholdType = "Frac"


G = CN.Erdos(n,p)

T,I = S.ComplexSim(G,InitialFrac,StoppingTime,gamma,beta,Threshold,ThresholdType)
