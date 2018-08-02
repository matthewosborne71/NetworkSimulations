import CreateNetworks as CN
import Simulation as S


n = 100
k = 5
p = .3

InitialFrac = .2
StoppingTime = 1
gamma = 10
beta = 1


G = CN.Erdos(n,p)

T,I = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)
