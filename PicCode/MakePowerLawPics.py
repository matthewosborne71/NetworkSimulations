import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods
import Path
import seaborn as sns

Time = 2

#kind = "BySimulation"
kind = "Incidence"

path = Path.GetHomePath()
SourceFile = r"SimulationResults\\Comparison_k_6\\Comparison_PowerLaw.csv"

SaveFolder = r"SimulationResults\\FOI_Pics\\ComparisonPics\\k_6\\"

if kind == "Incidence":
    a = pd.read_csv(path + SourceFile)
    a = a.loc[a.EventTime < Time,]
    a = a.sort_values(['exponent','Threshold','I'])

    Exps = list(set(a.exponent.values))
    Thresholds = list(set(a.Threshold.values))
    Exps.sort()
    Thresholds.sort()

    time = float(10)**(-2)

    row = 2
    col = 3
    xlim = (0,1000)

    for e in Exps:
        b = a.loc[a.exponent == e,]


        fig,ax = plt.subplots(row,col,sharex = 'col',sharey = 'row',figsize = [12,8])
        for i in range(len(Thresholds)):
            c = b.loc[b.Threshold == Thresholds[i],]
            if len(c) > 10:
                minI = c.I.values.min()
                maxI = c.I.values.max()
                xs = np.arange(minI,maxI,1)
                k = smooth.NonParamRegression(c.I.values,c.Inc.values,method = npr_methods.LocalPolynomialKernel(q=1),bandwidth = 50)
                k.fit()
                ax[i/col,i%col].plot(c.I.values,c.Inc.values,'.')
                ax[i/col,i%col].plot(xs,k(xs),'r-',linewidth = 2)
                ax[i/col,i%col].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
                ylim = ax[0,0].get_ylim()
                ax[i/col,i%col].set_ylim(ylim)
                ax[i/col,i%col].set_xlim(xlim)
            else:
                ax[i/col,i%col].plot(c.I.values,c.Inc.values,'.')
                ax[i/col,i%col].set_title("Threshold: " + str(np.round(Thresholds[i],4)))
                ylim = ax[0,0].get_ylim()
                ax[i/col,i%col].set_ylim(ylim)
                ax[i/col,i%col].set_xlim(xlim)

        fig.suptitle("Power Law - Configuration, Exponent: " + str(np.round(e,4)) + ", Time Round: " + str(time))
        fig.text(0.5,0.04,"I",ha = "center")
        fig.text(0.04,0.5,"Incidence",va = 'center',rotation = 'vertical')
        plt.savefig(path + SaveFolder + "PowerLawIncidence_exp_" + str(np.round(e,4)) + ".png")
        plt.close()
        del fig
        del ax
elif kind == "BySimulation":
    a = pd.read_csv(path + SourceFile)

    Exps = list(set(a.exponent.values))
    Thresholds = list(set(a.Threshold.values))
    SimNums = list(set(a.Sim.values))
    SimNums.sort()
    Exps.sort()
    Thresholds.sort()

    for e in Exps:
        b = a.loc[a.exponent == e,]
        for Threshold in Thresholds:
            c = b.loc[b.Threshold == Threshold,]
            g = sns.FacetGrid(data = c, col = 'Sim', col_wrap = 10)
            g = g.map(plt.scatter,"I","Inc",s = 2)

            plt.savefig(path + SaveFolder + r"BySimulation\\PowerLawBySimulation_exp_" + str(np.round(e,4)) +
                        "_Threshold" + str(np.round(Threshold,2)) + ".png")
            plt.close()
            del g
            del c
        del b
