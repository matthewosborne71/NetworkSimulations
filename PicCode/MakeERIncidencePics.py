import pandas as pd
import numpy as np
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods
import matplotlib.pyplot as plt
import Path

path = Path.GetHomePath()

a = pd.read_csv(path + r"SimulationResults\\Comparison_k_20\\Comparison_ERSims.csv")

Time = 2

a = a.loc[a.EventTime < Time,]
# Only use when trimming data
#a = a.loc[a.I <= 100,]


EdgeProbs = list(set(a.EdgeProb.values))
Thresholds = list(set(a.Threshold.values))
EdgeProbs.sort()
Thresholds.sort()

x = np.arange(10,1000.5,.5)
beta = 1.5
xlim = (0,1000)

for e in EdgeProbs:
    b = a.loc[a.EdgeProb == e,]

    if e < 0.1:
        time = float(10)**(-2)
    elif e < 0.3:
        time = float(10)**(-3)
    else:
        time = float(10)**(-3)

    y = beta * time * e * x *(1000 - x)

    col = 3
    row = 2
    fig,ax = plt.subplots(row,col,sharex = 'col',sharey = 'row',figsize = [12,8])
    for i in range(len(Thresholds)):
        c = b.loc[b.Threshold==Thresholds[i],]
        if len(c) > 10:
            minI = c.I.values.min()
            maxI = c.I.values.max()
            xs = np.arange(minI,maxI,1)
            # Untrimmed regression
            #k = smooth.NonParamRegression(c.I.values,c.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
            # Trimmed Regression
            k = smooth.NonParamRegression(c.I.values,c.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
            k.fit()
            ax[i/col,i%col].plot(c.I.values,c.Inc.values,'.')
            ax[i/col,i%col].plot(xs,k(xs),'r-',linewidth = 2)
            #ax[i/5,i%5].set_xlim([0,100])
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



    fig.suptitle("Erdos Renyi, Edge Probability: " + str(e) + ", Time Round: " + str(time))
    fig.text(0.5,0.04,"I",ha = "center")
    fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
    # Untrimmed
    #plt.savefig(path + r"SimulationResults\\FOI_Pics\\ER\\ER_Incidence_EP_" + str(e) + ".png")
    # Trimmed
    plt.savefig(path + r"SimulationResults\\FOI_Pics\\ComparisonPics\\k_20\\ER_Incidence_EP_" + str(e) + ".png")
    plt.close()
    del fig
    del ax
