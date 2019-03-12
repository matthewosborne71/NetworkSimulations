import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods
import Path

path = Path.GetHomePath()

a = pd.read_csv(path + r"SimulationResults\\RData_Lattice.csv")

Thresholds = list(set(a.Threshold.values))
Thresholds.sort()
Ns = list(set(a.N.values))
Ns.sort()
Ms = []
for i in range(len(Ns)):
    Ms.append(1000/Ns[i])

time = float(10)**(-1)



for P in [True,False]:
    b = a.loc[a.Periodic == P,]
    if P == True:
        Path = path + r"SimulationResults\\FOI_Pics\\PeriodicLattice\\"
    else:
        Path = path + r"SimulationResults\\FOI_Pics\\Lattice\\"
    for n in range(len(Ns)):
        c = b.loc[b.N == Ns[n],]
        fig,ax = plt.subplots(2,2,sharex = 'col',sharey = 'row',figsize = [12,8])
        for i in range(4):
            print(i)
            d = c.loc[c.Threshold == Thresholds[i],]
            if len(d) > 10:
                minI = d.I.values.min()
                maxI = d.I.values.max()
                xs = np.arange(minI,maxI,1)
                k = smooth.NonParamRegression(d.I.values,d.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 100)
                k.fit()
                ax[i/2,i%2].plot(d.I.values,d.Inc.values,'.')
                ax[i/2,i%2].plot(xs,k(xs),'-r',linewidth = 2)
                ax[i/2,i%2].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
                ylim = ax[0,0].get_ylim()
                ax[i/2,i%2].set_ylim(ylim)
                ax[i/2,i%2].set_xlim((0,1000))

        if P == True:
            fig.suptitle(str(Ns[n]) + " by " + str(Ms[n]) + " Periodic Lattice, Time Round: " + str(time))
        else:
            fig.suptitle(str(Ns[n]) + " by " + str(Ms[n]) + " Lattice, Time Round: " + str(time))
        fig.text(0.5,0.04,"I",ha = "center")
        fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
        plt.savefig(Path + str(Ns[n]) + "_" + str(Ms[n]) + "_Incidence.png")
        plt.savefig(Path + str(Ns[n]) + "_" + str(Ms[n]) + "_Incidence.png")
        plt.close()
