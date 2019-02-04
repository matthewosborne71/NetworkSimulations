import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Path

path = Path.GetHomePath()

a = pd.read_csv(path + r"SimulationResults\\RData_BlockModel.csv")

Parts = list(set(a.Partition.values))
Thresholds = list(set(a.Threshold.values))
Thresholds.sort()

time = float(10)**(-2)

minI = a.I.values.min()
maxI = a.I.values.max()
xs = np.arange(minI,maxI,1)

i = 0
for part in Parts:
    b = a.loc[a.Partition == part,]

    fig,ax = plt.subplots(3,4,sharex = 'col',sharey = 'row',figsize = [12,8])
    for i in range(len(Thresholds)):
        print str(i/4)+ " , " + str(i%4)
        c = b.loc[b.Threshold == Thresholds[i],]
        ax[i/4,i%4].plot(c.I.values,c.Inc.values,'.')
        ax[i/4,i%4].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
        ylim = ax[0,0].get_ylim()
        ax[i/4,i%4].set_ylim(ylim)
        ax[i/4,i%4].set_xlim((0,1000))

    fig.suptitle("Small World, Partition: " + str(part) + ", Time Round: " + str(time))
    fig.text(0.5,0.04,"I",ha = "center")
    fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
    plt.savefig(path + r"SimulationResults\\FOI_Pics\\BlockModel\\BlockModel_Incidence_" + str(i) + ".png")
    plt.close()
    i = i + 1
    del fig
    del ax
