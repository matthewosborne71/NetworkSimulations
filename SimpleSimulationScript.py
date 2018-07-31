import CreateNetworks as CN
import Simulation as S


n = 1000
k = 5
p = .3

InitialFrac = .1
StoppingTime = 10
gamma = 2
beta = 1


G = CN.SmallWorld(n,k,p)

T,I = S.SimpleSim(G,InitialFrac,StoppingTime,gamma,beta)
