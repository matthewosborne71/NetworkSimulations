import pandas as pd
import Path

First = True
path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexComparison_NegativeBinomial.csv"
SimpleFile = "SimulationResults/SimpleComparison_NegativeBinomial.csv"
CSV_Save_Name = "SimulationResults/Comparison_NegativeBinomial.csv"

Complex = pd.read_csv(path + ComplexFile)
Simple = pd.read_csv(path + SimpleFile)
Simple['Threshold'] = 0
Simple = Simple[Complex.columns]

All = pd.concat([Simple,Complex])

del Complex
del Simple

Round = 2

All['Round'] = All['EventTime'].round(Round)


Nums = list(set(All.Num_Success.values))
Thresholds = list(set(All.Threshold.values))
SimNums = list(set(All.SimNum.values))
SimNums.sort()
Nums.sort()
Thresholds.sort()

for num in Nums:
    ThatNum = All.loc[All.Num_Success == num,]
    probs = list(set(ThatNum.Prob.values))
    probs.sort()
    for p in probs:
        AllEvents = ThatNum.loc[ThatNum.Prob == p,]
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
                RData = RData.sort_values(['I'])
                RData['Num_Success'] = num
                RData['Prob'] = p
                RData['Threshold'] = Threshold
            else:
                A = pd.DataFrame({'Sim':Sims,'I':I,'Inc':Inc,'EventTime':Times})
                del I
                del Inc
                del Sims
                A.sort_values(['I'])
                A['Num_Success'] = num
                A['Prob'] = p
                A['Threshold'] = Threshold
                RData = pd.concat([RData,A])
                del A

        del AllEvents
    del ThatNum

RData = RData[['Prob','Num_Success','Threshold','Sim','I','Inc','EventTime']]
RData = RData.sort_values(['Prob','Num_Success','Threshold','Sim','I'])

RData.to_csv(path + CSV_Save_Name,index = False)
