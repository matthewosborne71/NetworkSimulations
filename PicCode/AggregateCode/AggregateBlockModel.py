import pandas as pd
import logging
import Path


path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexContagionSimulations_BlockModel3.csv"
SimpleFile = "SimulationResults/SimpleContagionSimulations_BlockModel3.csv"
CSV_Save_Names = ["SimulationResults/Comparison_BlockModel3.csv",
                    "SimulationResults/Comparison_BlockModel3_Partition_0.csv",
                    "SimulationResults/Comparison_BlockModel3_Partition_1.csv",
                    "SimulationResults/Comparison_BlockModel3_Partition_2.csv"]

FileTypes = ["Full","0","1","2"]

Complex = pd.read_csv(path + ComplexFile)
Simple = pd.read_csv(path + SimpleFile)
Simple['Threshold'] = 0
Simple = Simple[Complex.columns]

All = pd.concat([Simple,Complex])

del Complex
del Simple

Round = 2

All['Round'] = All['EventTime'].round(Round)

Parts = list(set(All.Partition.values))
Thresholds = list(set(All.Threshold.values))
Thresholds.sort()
SimNums = list(set(All.SimNum.values))
SimNums.sort()

Total = len(Parts)*len(Thresholds)*len(SimNums)

def PartitionAgg(PartitionInfect,SaveFile):
    First = True
    for part in Parts:
        AllEvents = All.loc[All.Partition == part,]

        for Threshold in Thresholds:
            TheseEvents = AllEvents.loc[AllEvents.Threshold == Threshold,]

            I = []
            Inc = []
            Times = []

            for Sim in SimNums:
                ThisSim = TheseEvents.loc[TheseEvents.SimNum == Sim,]
                c = ThisSim.groupby('Round').mean()['CurrentI']
                d = ThisSim.loc[ThisSim.PartitionEvent == PartitionInfect,'Round'].value_counts()
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
                del Inc
                del Times
                RData = RData.sort_values(['I'])
                RData['Partition'] = part
                RData['Threshold'] = Threshold
            else:
                A = pd.DataFrame({'I':I,'Inc':Inc,'EventTime':Times})
                del I
                del Inc
                del Times
                A.sort_values(['I'])
                A['Partition'] = part
                A['Threshold'] = Threshold
                RData = pd.concat([RData,A])
                del A

        del AllEvents

    RData.to_csv(path + SaveFile,index = False)

def FullAggregate(SaveFile):
    First = True
    for part in Parts:
        AllEvents = All.loc[All.Partition == part,]

        for Threshold in Thresholds:
            TheseEvents = AllEvents.loc[AllEvents.Threshold == Threshold,]

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
                del Inc
                del Times
                RData = RData.sort_values(['I'])
                RData['Partition'] = part
                RData['Threshold'] = Threshold
            else:
                A = pd.DataFrame({'I':I,'Inc':Inc,'EventTime':Times})
                del I
                del Inc
                del Times
                A.sort_values(['I'])
                A['Partition'] = part
                A['Threshold'] = Threshold
                RData = pd.concat([RData,A])
                del A

        del AllEvents

    RData.to_csv(path + SaveFile,index = False)

for i in range(len(FileTypes)):
    Type = FileTypes[i]
    SaveFile = CSV_Save_Names[i]
    if Type == "Full":
        FullAggregate(SaveFile)
    else:
        PartitionAgg("Partition" + Type + "_Infection",SaveFile)
