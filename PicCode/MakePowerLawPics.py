import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods
import Path

path = Path.GetHomePath()

a = pd.read_csv(path + r"SimulationResults\\RData_PowerLaw.csv")

Exps = list(set(a.exponent.values))
Thresholds = list(set(a.Threshold.values))
Exps.sort()
Thresholds.sort()

time = float(10)**(-2)

for e in Exps:
    b = a.loc[a.exponent == e,]

    fig,ax = plt.subplots(4,5,sharex = 'col',sharey = 'row',figsize = [12,8])
    for i in range(len(Thresholds)):
        c = b.loc[b.Threshold == Thresholds[i],]
        if len(c) > 10:
            minI = c.I.values.min()
            maxI = c.I.values.max()
            xs = np.arange(minI,maxI,1)
            k = smooth.NonParamRegression(c.I.values,c.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
            k.fit()
            ax[i/5,i%5].plot(c.I.values,c.Inc.values,'.')
            ax[i/5,i%5].plot(xs,k(xs),'r-',linewidth = 2)
            ax[i/5,i%5].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
            ylim = ax[0,0].get_ylim()
            ax[i/5,i%5].set_ylim(ylim)
            ax[i/5,i%5].set_xlim((0,1000))
        else:
            ax[i/5,i%5].plot(c.I.values,c.Inc.values,'.')
            ax[i/5,i%5].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
            ylim = ax[0,0].get_ylim()
            ax[i/5,i%5].set_ylim(ylim)
            ax[i/5,i%5].set_xlim((0,1000))

    fig.suptitle("Power Law - Configuration, Exponent: " + str(np.round(e,4)) + ", Time Round: " + str(time))
    fig.text(0.5,0.04,"I",ha = "center")
    fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
    plt.savefig(path + r"SimulationResults\\FOI_Pics\\PowerLaw\\PowerLawIncidence_exp_" + str(np.round(e,4)) + ".png")
    plt.close()
    del fig
    del ax
