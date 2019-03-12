import pandas as pd
import Path

First = True
path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexContagionSimulations_Lobster.csv"
SimpleFile = "SimulationResults/SimpleContagionSimulations_Lobster.csv"
CSV_Save_Name = "SimulationResults/RData_Lobster.csv"

Round = 1

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
p1s = list(set(All.p1.values))
p1s.sort()
p2s = list(set(All.p2.values))
p2s.sort()

for p1 in p1s:
    ALLEvents = All.loc[All.p1 == p1,]
    for p2 in p2s:
        AllEvents = ALLEvents.loc[ALLEvents.p2 == p2,]
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
                RData['Threshold'] = Threshold
                RData['p1'] = p1
                RData['p2'] = p2
            else:
                A = pd.DataFrame({'I':I,'Inc':Inc})
                del I
                del Inc
                A['Threshold'] = Threshold
                A['p1'] = p1
                A['p2'] = p2
                RData = pd.concat([RData,A])
                del A
        del AllEvents
    del ALLEvents
del All

RData = RData[['p1','p2','Threshold','I','Inc']]
RData = RData.sort_values(['p1','p2','Threshold','I'])
RData.to_csv(path + CSV_Save_Name,index = False)
