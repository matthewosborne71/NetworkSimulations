import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods
import Path

path = Path.GetHomePath()

a = pd.read_csv(path + r"SimulationResults\\Comparison_RandomRegular.csv")

Thresholds = list(set(a.Threshold.values))
Thresholds.sort()

time = float(10)**(-2)

row = 2
col = 3
xlim = (0,1000)

fig,ax = plt.subplots(2,3,sharex = 'col',sharey = 'row',figsize = [12,8])
for i in range(len(Thresholds)):
    c = a.loc[a.Threshold == Thresholds[i],]
    if len(c) > 10:
        minI = c.I.values.min()
        maxI = c.I.values.max()
        xs = np.arange(minI,maxI,1)
        k = smooth.NonParamRegression(c.I.values,c.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
        k.fit()
        ax[i/col,i%col].plot(c.I.values,c.Inc.values,'.')
        ax[i/col,i%col].plot(xs,k(xs),'-r',linewidth = 2)
        ax[i/col,i%col].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
        ylim = ax[0,0].get_ylim()
        ax[i/col,i%col].set_ylim(ylim)
        ax[i/col,i%col].set_xlim(xlim)

fig.suptitle("Random Regular, Time Round: " + str(time))
fig.text(0.5,0.04,"I",ha = "center")
fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
plt.savefig(path + r"SimulationResults\\FOI_Pics\\ComparisonPics\\RandomRegular_Incidence.png")
plt.close()
