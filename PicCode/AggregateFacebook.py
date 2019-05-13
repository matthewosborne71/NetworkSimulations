import pandas as pd
import Path

First = True
path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexContagionSimulations_Facebook.csv"
SimpleFile = "SimulationResults/SimpleContagionSimulations_Facebook.csv"
CSV_Save_Name = "SimulationResults/Comparison_Facebook.csv"

Round = 2

Complex = pd.read_csv(path + ComplexFile)
Simple = pd.read_csv(path + SimpleFile)

Simple['Threshold'] = 0
Simple = Simple[list(Complex.columns)]

All = pd.concat([Simple,Complex])

del Simple
del Complex

Thresholds = list(set(All.Threshold.values))
Thresholds.sort()
SimNums = list(set(All.SimNum.values))
SimNums.sort()

All['Round'] = All['EventTime'].round(Round)

for Threshold in Thresholds:
    TheseEvents = All.loc[All.Threshold == Threshold,]
    I = []
    Inc = []
    Times = []

    for Sim in SimNums:
        ThisSim = TheseEvents.loc[TheseEvents.SimNum == Sim,]
        c = ThisSim.groupby('Round').mean()['CurrentI']
        d = ThisSim.loc[ThisSim.Event == "Infection",'Round'].value_counts()
        for i in d.index:
            I.append(c[i])
            Inc.append(d[i])
            Times.append(i)

        del c
        del d
        del ThisSim

    del TheseEvents

    if First:
        First = False
        RData = pd.DataFrame({'I':I,'Inc':Inc,'EventTime':Times})
        del I
        del Times
        del Inc
        RData['Threshold'] = Threshold
    else:
        A = pd.DataFrame({'I':I,'Inc':Inc,'EventTime':Times})
        del I
        del Times
        del Inc
        A['Threshold'] = Threshold
        RData = pd.concat([RData,A])
        del A

del All

RData = RData[['Threshold','I','Inc','EventTime']]
RData = RData.sort_values(['Threshold','I'])
RData.to_csv(path+CSV_Save_Name,index = False)
