import pandas as pd
import Path

First = True
path = Path.GetPath()
ComplexFile = "SimulationResults/ComplexComparison_PowerLaw.csv"
SimpleFile = "SimulationResults/SimpleComparison_PowerLaw.csv"
CSV_Save_Name = "SimulationResults/Comparison_PowerLaw.csv"

Round = 1

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
exps = list(set(All.exponent.values))
exps.sort()

All['Round'] = All['EventTime'].round(Round)

for e in exps:
	AllEvents = All.loc[All.exponent == e,]
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
			RData['exponent'] = e
		else:
			A = pd.DataFrame({'Sim':Sims,'I':I,'Inc':Inc,'EventTime':Times})
			del I
			del Inc
			del Sims
			A['Threshold'] = Threshold
			A['exponent'] = e
			RData = pd.concat([RData,A])
			del A
	del AllEvents
del All

RData = RData[['exponent','Threshold','Sim','I','Inc','EventTime']]
RData = RData.sort_values(['exponent','Threshold','Sim','I'])
RData.to_csv(path + CSV_Save_Name,index=False)
