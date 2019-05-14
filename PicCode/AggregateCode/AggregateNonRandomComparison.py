import pandas as pd
import Path

path = Path.GetPath()
CSV_Save_Name = "SimulationResults/Aggregate_NonRandom.csv"

Round = 1


SimResults = pd.read_csv(path + "SimulationResults/ComparisonNonRandom.csv",quotechar="'")
SimResults['Round'] = SimResults['EventTime'].round(Round)

NetworkTypes = list(set(SimResults.NetworkType.values))
SimNums = list(set(SimResults.SimNum.values))

First = True

for Type in NetworkTypes:
    TypeSims = SimResults.loc[SimResults.NetworkType == Type,]
    Features = list(set(TypeSims.FeatureStat))
    for Feature in Features:
        FeatureSims = TypeSims.loc[TypeSims.FeatureStat == Feature,]
        Thresholds = list(set(FeatureSims.Threshold.values))
        Thresholds.sort()
        for Threshold in Thresholds:
            AllEvents = FeatureSims.loc[FeatureSims.Threshold == Threshold,]
            I = []
            Inc = []

            for Sim in SimNums:
                ThisSim = AllEvents.loc[AllEvents.SimNum == Sim,]
                c = ThisSim.groupby('Round').mean()['CurrentI']
                d = ThisSim.loc[ThisSim.Event == "Infection",'Round'].value_counts()
                for i in d.index:
                    I.append(c[i])
                    Inc.append(d[i])

                del c
                del d
                del ThisSim

            del AllEvents

            if First:
                First = False
                Data = pd.DataFrame({'I':I,'Inc':Inc})
                del I
                del Inc
                Data['NetworkType'] = Type
                Data['FeatureStat'] = Feature
                Data['Threshold'] = Threshold
            else:
                A = pd.DataFrame({'I':I,'Inc':Inc})
                del I
                del Inc
                A['NetworkType'] = Type
                A['FeatureStat'] = Feature
                A['Threshold'] = Threshold
                Data = pd.concat([Data,A])
                del A
        del FeatureSims
    del TypeSims

Data = Data[['NetworkType','FeatureStat','Threshold','I','Inc']]
Data = Data.sort_values(['NetworkType','FeatureStat','Threshold','I'])
Data.to_csv(path + CSV_Save_Name,index = False)
