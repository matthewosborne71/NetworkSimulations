import pandas as pd
import numpy as np
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods
import matplotlib.pyplot as plt
import Path

path = Path.GetHomePath()

Time = 2

DataName = "SimulationResults/Comparison_Blocks/Comparison_BA_BA.csv"
DataName0 = "SimulationResults/Comparison_Blocks/Comparison_BA_BA_Partition_0.csv"
DataName1 = "SimulationResults/Comparison_Blocks/Comparison_BA_BA_Partition_1.csv"

SaveStarter = "SimulationResults/FOI_Pics/ComparisonPics/BlockModels/BA_BA_Incidence_"

a = pd.read_csv(path + DataName)
a0 = pd.read_csv(path + DataName0)
a1 = pd.read_csv(path + DataName1)

a = a.loc[a.EventTime < Time, ]
a0 = a0.loc[a0.EventTime < Time, ]
a1 = a1.loc[a1.EventTime < Time, ]

Parts = list(set(a.Partition.values))
Thresholds = list(set(a.Threshold.values))
Thresholds.sort()

time = float(10)**(-1)

minI = a.I.values.min()
maxI = a.I.values.max()
xs = np.arange(minI,maxI,1)

j = 0
col = 4
row = 3
xlim = (0,2000)
for part in Parts:
    b = a.loc[a.Partition == part,]
    b0 = a0.loc[a0.Partition == part,]
    b1 = a1.loc[a1.Partition == part,]

    fig,ax = plt.subplots(row,col,sharex = 'col',sharey = 'row',figsize = [12,8])
    for i in range(len(Thresholds)):
        c = b.loc[b.Threshold==Thresholds[i],]
        c0 = b0.loc[b0.Threshold==Thresholds[i],]
        c1 = b1.loc[b1.Threshold==Thresholds[i],]

        if len(c) > 10:
            minI = c.I.values.min()
            maxI = c.I.values.max()
            xs = np.arange(minI,maxI,1)
            # k = smooth.NonParamRegression(c.I.values,c.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
            # k.fit()
            # k0 = smooth.NonParamRegression(c0.I.values,c0.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
            # k0.fit()
            # k1 = smooth.NonParamRegression(c1.I.values,c1.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
            # k1.fit()
            ax[i/col,i%col].plot(c.I.values,c.Inc.values,'k.',label = 'Whole Network')
            ax[i/col,i%col].plot(c0.I.values,c0.Inc.values,'r.',label = 'Block 0')
            ax[i/col,i%col].plot(c1.I.values,c1.Inc.values,'b.',label = 'Block 1')
            # ax[i/col,i%col].plot(xs,k(xs),'k-',linewidth = 2,label = 'Whole Network')
            # ax[i/col,i%col].plot(xs,k0(xs),'r-',linewidth = 2,label = 'Block 0')
            # ax[i/col,i%col].plot(xs,k1(xs),'b-',linewidth = 2,label = 'Block 1')
            ylim = ax[0,0].get_ylim()
            ax[i/col,i%col].set_ylim(ylim)
            ax[i/col,i%col].set_xlim(xlim)
            ax[i/col,i%col].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
        else:
            ax[i/col,i%col].plot(c.I.values,c.Inc.values,'.')
            #ax[i/5,i%5].set_xlim([0,100])
            ylim = ax[0,0].get_ylim()
            ax[i/col,i%col].set_ylim(ylim)
            ax[i/col,i%col].set_xlim(xlim)
            ax[i/col,i%col].set_title("Threshold: " + str(np.round(Thresholds[i],4)))

    fig.suptitle("BA BA Block Model, Partition: " + str(part) + ", Time Round: " + str(time))
    fig.text(0.5,0.04,"I",ha = "center")
    fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
    plt.savefig(path + SaveStarter + part + ".png")
    plt.close()
    del fig
    del ax
