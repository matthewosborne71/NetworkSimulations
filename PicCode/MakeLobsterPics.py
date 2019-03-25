import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods
import Path

path = Path.GetHomePath()

a = pd.read_csv(path + r"SimulationResults\\RData_Lobster.csv")

Thresholds = list(set(a.Threshold.values))
Thresholds.sort()
p1s = list(set(a.p1.values))
p1s.sort()
p2s = list(set(a.p2.values))
p2s.sort()

time = float(10)**(-2)

for p1 in p1s:
    b = a.loc[a.p1 == p1,]
    for p2 in p2s:
        c = b.loc[b.p2 == p2,]

        fig,ax = plt.subplots(2,4,sharex = 'col',sharey = 'row',figsize = [12,8])
        for i in range(8):
            print(i/2)
            print(i%4)
            print(">")
            d = c.loc[c.Threshold == Thresholds[i],]
            if len(d) > 10:
                minI = d.I.values.min()
                maxI = d.I.values.max()
                xs = np.arange(minI,maxI,1)
                k = smooth.NonParamRegression(d.I.values,d.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
                k.fit()
                ax[i/4,i%4].plot(d.I.values,d.Inc.values,'.')
                ax[i/4,i%4].plot(xs,k(xs),'-r',linewidth = 2)
                ax[i/4,i%4].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
                ylim = ax[0,0].get_ylim()
                ax[i/4,i%4].set_ylim(ylim)
                ax[i/4,i%4].set_xlim((0,300))

        fig.suptitle("Random Lobster, p1: " + str(np.round(p1,4)) + " p2: " + str(np.round(p2,4)) + ", Time Round: " + str(time))
        fig.text(0.5,0.04,"I",ha = "center")
        fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
        plt.savefig(path + r"SimulationResults\\FOI_Pics\\Lobster\\Lobster_" + str(np.round(p1,4)) + "_" + str(np.round(p2,4)) + "_Incidence.png")
        plt.close()
