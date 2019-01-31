import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods

path = Path.GetHomePath()

a = pd.read_csv(path + r"SimulationResults\\RData_SmallWorld.csv")

RewiringProbs = list(set(a.RewiringProb.values))
Thresholds = list(set(a.Threshold.values))
RewiringProbs.sort()
Thresholds.sort()

time = float(10)**(-2)

minI = a.I.values.min()
maxI = a.I.values.max()
xs = np.arange(minI,maxI,1)


for p in RewiringProbs:
    b = a.loc[a.RewiringProb == p,]

    fig,ax = plt.subplots(3,4,sharex = 'col',sharey = 'row',figsize = [12,8])
    for i in range(len(Thresholds)):
        print str(i/4)+ " , " + str(i%4)
        c = b.loc[b.Threshold == Thresholds[i],]
        if len(c) > 10:
            minI = c.I.values.min()
            maxI = c.I.values.max()
            xs = np.arange(minI,maxI,1)
            k = smooth.NonParamRegression(c.I.values,c.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1))
            k.fit()

            ax[i/4,i%4].plot(c.I.values,c.Inc.values,'.')
            ax[i/4,i%4].plot(xs,k(xs),'r-',linewidth = 2)
            ax[i/4,i%4].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
            ylim = ax[0,0].get_ylim()
            ax[i/4,i%4].set_ylim(ylim)
        else:
            ax[i/4,i%4].plot(c.I.values,c.Inc.values,'.')
            ax[i/4,i%4].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
            ylim = ax[0,0].get_ylim()
            ax[i/4,i%4].set_ylim(ylim)

    fig.suptitle("Small World, RewiringProb: " + str(np.round(p,4)) + ", Time Round: " + str(time))
    fig.text(0.5,0.04,"I",ha = "center")
    fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
    plt.savefig(path + r"SimulationResults\\FOI_Pics\\SmallWorld\\SmallWorldIncidence_RP_" + str(np.round(p,4)) + ".png")
    plt.close()
    del fig
    del ax
