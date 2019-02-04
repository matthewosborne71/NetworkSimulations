import pandas as pd
import logging
import Path

First = True
path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexContagionSimulations_BlockModel.csv"
SimpleFile = "SimulationResults/SimpleContagionSimulations_BlockModel.csv"
CSV_Save_Name = "SimulationResults/RData_BlockModel.csv"

Complex = pd.read_csv(path + ComplexFile)
Simple = pd.read_csv(path + SimpleFile)
Simple['Threshold'] = 0
Simple = Simple[Complex.columns]

All = pd.concat([Simple,Complex])

del Complex
del Simple

Round = 1

All['Round'] = All['EventTime'].round(Round)

Parts = list(set(All.Partition.values))
Thresholds = list(set(All.Threshold.values))
Thresholds.sort()
SimNums = list(set(All.SimNum.values))
SimNums.sort()

Total = len(Parts)*len(Thresholds)*len(SimNums)


for part in Parts:
    AllEvents = All.loc[All.Partition == part,]

    for Threshold in Thresholds:
        TheseEvents = AllEvents.loc[AllEvents.Threshold == Threshold,]

        I = []
        Inc = []

        for Sim in SimNums:
            ThisSim = TheseEvents.loc[TheseEvents.SimNum == Sim,]
            c = ThisSim.groupby('Round').mean()['CurrentI']
            d = ThisSim.loc[ThisSim.Event == "Infection",'Round'].value_counts()
            for i in d.index:
                I.append(c[i])
                Inc.append(d[i])

            del c
            del d
            del ThisSim

        del TheseEvents

        if First:
            First = False
            RData = pd.DataFrame({'I':I,'Inc':Inc})
            del I
            del Inc
            RData = RData.sort_values(['I'])
            RData['Partition'] = part
            RData['Threshold'] = Threshold
        else:
            A = pd.DataFrame({'I':I,'Inc':Inc})
            del I
            del Inc
            A.sort_values(['I'])
            A['Partition'] = part
            A['Threshold'] = Threshold
            RData = pd.concat([RData,A])
            del A

    del AllEvents

RData.to_csv(path + CSV_Save_Name,index = False)
