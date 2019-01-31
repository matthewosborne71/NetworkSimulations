import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Path

path = Path.GetHomePath()

a = pd.read_csv(path + r"SimulationResults\\RData_ERSims.csv")

EdgeProbs = list(set(a.EdgeProb.values))
Thresholds = list(set(a.Threshold.values))
EdgeProbs.sort()
Thresholds.sort()

x = np.arange(10,1000.5,.5)
beta = 1.5

for e in EdgeProbs:
    b = a.loc[a.EdgeProb == e,]

    if e < 0.1:
        time = float(10)**(-2)
    elif e < 0.3:
        time = float(10)**(-3)
    else:
        time = float(10)**(-3)

    y = beta * time * e * x *(1000 - x)

    fig,ax = plt.subplots(4,5,sharex = 'col',sharey = 'row',figsize = [12,8])
    for i in range(20):
        c = b.loc[b.Threshold==Thresholds[i],]
        ax[i/5,i%5].plot(c.I.values,c.Inc.values,'.')
        ax[i/5,i%5].plot(x,y,'r-')
        #ax[i/5,i%5].set_xlim([0,100])
        ylim = ax[0,0].get_ylim()
        ax[i/5,i%5].set_ylim(ylim)
        ax[i/5,i%5].set_title("Threshold: " + str(np.round(Thresholds[i],4)))

    fig.suptitle("Erdos Renyi, Edge Probability: " + str(e) + ", Time Round: " + str(time))
    fig.text(0.5,0.04,"I",ha = "center")
    fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
    plt.savefig(path + r"SimulationResults\\FOI_Pics\\ER\\ER_Incidence_EP_" + str(e) + ".png")
    plt.close()
    del fig
    del ax
