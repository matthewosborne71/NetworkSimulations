import pandas as pd
import Path

First = True
path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexContagionSimulations_SmallWorldNewman.csv"
SimpleFile = "SimulationResults/SimpleContagionSimulations_SmallWorldNewman.csv"
CSV_Save_Name = "SimulationResults/RData_SmallWorldNewman.csv"

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
ShortCutProbs = list(set(All.ShortCutProb.values))
ShortCutProbs.sort()

Total = len(Thresholds)*len(SimNums)

for p in ShortCutProbs:
	AllEvents = All.loc[All.ShortCutProb == p,]
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
			RData['ShortCutProb'] = p
		else:
			A = pd.DataFrame({'I':I,'Inc':Inc})
			del I
			del Inc
			A['Threshold'] = Threshold
			A['ShortCutProb'] = p
			RData = pd.concat([RData,A])
			del A
	del AllEvents
del All

RData = RData[['ShortCutProb','Threshold','I','Inc']]
RData = RData.sort_values(['ShortCutProb','Threshold','I'])
RData.to_csv(path + CSV_Save_Name,index=False)
