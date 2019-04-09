import pandas as pd
import logging
import Path

First = True
path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexComparison_ER.csv"
SimpleFile = "SimulationResults/SimpleComparison_ER.csv"
CSV_Save_Name = "SimulationResults/Comparison_ERSims.csv"

logging.basicConfig(filename = path + "Logs/RDataER.log",
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)

logging.info("Reading in Data\n")

Complex = pd.read_csv(path + ComplexFile)
Simple = pd.read_csv(path + SimpleFile)

Simple['Threshold'] = 0

All = pd.concat([Simple,Complex])

del Complex
del Simple

EdgeProbs = list(set(All.EdgeProb.values))
EdgeProbs.sort()
Thresholds = list(set(All.Threshold.values))
Thresholds.sort()
SimNums = list(set(All.SimNum.values))
SimNums.sort()

Total = len(EdgeProbs)*len(Thresholds)*len(SimNums)

logging.info("About to aggregate the data for R.\n")

i = 0

for EdgeProb in EdgeProbs:
    logging.info("Running for EdgeProb: " + str(EdgeProb) + "\n")
    AllEvents = All.loc[All.EdgeProb == EdgeProb,]
    if EdgeProb < 0.1:
        AllEvents['Round'] = AllEvents['EventTime'].round(1)
    elif EdgeProb < 0.3:
        AllEvents['Round'] = AllEvents['EventTime'].round(3)
    else:
        AllEvents['Round'] = AllEvents['EventTime'].round(3)
    for Threshold in Thresholds:
        logging.info("Running for Threshold: " + str(Threshold) + "\n")
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
            i = i + 1

        del TheseEvents

        if First:
            First = False
            RData = pd.DataFrame({'I':I,'Inc':Inc})
            del I
            del Inc
            RData['EdgeProb'] = EdgeProb
            RData['Threshold'] = Threshold
        else:
            A = pd.DataFrame({'I':I,'Inc':Inc})
            del I
            del Inc
            A['EdgeProb'] = EdgeProb
            A['Threshold'] = Threshold
            RData = pd.concat([RData,A])
            del A

    del AllEvents

RData = RData[['EdgeProb','Threshold','I','Inc']]
RData = RData.sort_values(['EdgeProb','Threshold','I'])
RData.to_csv(path + CSV_Save_Name,index = False)
