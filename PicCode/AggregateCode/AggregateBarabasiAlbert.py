import pandas as pd
import Path

First = True
path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexComparison_BA.csv"
SimpleFile = "SimulationResults/SimpleComparison_BA.csv"
CSV_Save_Name = "SimulationResults/Comparison_BA.csv"

Round = 2

Complex = pd.read_csv(path + ComplexFile)
Simple = pd.read_csv(path + SimpleFile)

Simple['Threshold'] = 0
Simple = Simple[list(Complex.columns)]

All = pd.concat([Simple,Complex])

del Simple
del Complex

All['Round'] = All['EventTime'].round(Round)

Thresholds = list(set(All.Threshold.values))
Thresholds.sort()
SimNums = list(set(All.SimNum.values))
SimNums.sort()
ms = list(set(All.m.values))
ms.sort()

All['Round'] = All['EventTime'].round(Round)

for m in ms:
    AllEvents = All.loc[All.m == m,]
    for Threshold in Thresholds:
        TheseEvents = AllEvents.loc[AllEvents.Threshold == Threshold,]
        I = []
        Inc = []
        Sims = []
        Times = []

        for Sim in SimNums:
            ThisSim = TheseEvents.loc[TheseEvents.SimNum == Sim,]
            c = ThisSim.groupby('Round').mean()['CurrentI']
            d = ThisSim.loc[ThisSim.Event == "Infection",'Round'].value_counts()
            for i in d.index:
                I.append(c[i])
                Inc.append(d[i])
                Sims.append(Sim)
                Times.append(i)

            del c
            del d
            del ThisSim

        del TheseEvents

        if First:
            First = False
            RData = pd.DataFrame({'Sim':Sims,'I':I,'Inc':Inc,'EventTime':Times})
            del I
            del Inc
            del Sims
            RData['Threshold'] = Threshold
            RData['m'] = m
        else:
            A = pd.DataFrame({'Sim':Sims,'I':I,'Inc':Inc,'EventTime':Times})
            del I
            del Inc
            del Sims
            A['Threshold'] = Threshold
            A['m'] = m
            RData = pd.concat([RData,A])
            del A
    del AllEvents
del All

RData = RData[['m','Threshold','Sim','I','Inc','EventTime']]
RData = RData.sort_values(['m','Threshold','Sim','I'])
RData.to_csv(path+CSV_Save_Name,index = False)
