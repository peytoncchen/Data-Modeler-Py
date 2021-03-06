# Results object to store generated results from calculations 

# Copyright (C) 2020 Peyton Chen

import random
import scipy.stats as sc


class Results:
    def __init__(self):
        self.errorResults = []
        self.dVObjects = []
        self.dVResults = []
        self.multiRun = []
        self.resultframes = []
        self.fresults = []
        self.fpwrstring = ''
        self.pstring = ''
        self.fstring = ''


    def addRun(self):
        #Adding results from current dVResults into multiRun so user can store multiple runs
        results = self.dVResults
        self.multiRun.append(results)


    def cleardVResultView(self):
        #Clearing the dVVal View when the current displayed values are not up to date/irrelevant
        length = len(self.dVResults)
        self.dVResults.clear()
        for i in range(length):
            self.dVResults.append('')


    def gendvVals(self, s5inputs, s4inputs, totalerror):
        #Generates dependent variable values using Gaussian distribution (inv-norm) and user inputs
        count = len(s5inputs[0])
        numBF = len(s5inputs[1][0])
        result = []
        for i in range(count):
            dvVal = 0.0
            tNum = int(s5inputs[0][i])
            dvVal += float(s4inputs[tNum-1]) #adding treatment value

            rand = random.uniform(0.0, 1.0)

            if float(totalerror) != 0: #Handling case where totalerror = 0 then don't run this code
                tEVal = sc.norm(0, float(totalerror)).ppf(rand)
                dvVal += tEVal #adding generated total error value based on totalerror SD value

            for j in range(numBF):
                bFnum = int(s5inputs[1][i][j])
                dvVal += self.errorResults[j][bFnum-1]
            
            rounded = round(dvVal, 4)
            result.append(rounded)
        
        self.dVResults = result


    def genEVals(self, s2inputs, s3inputs):
        #Based on number associated with each blocking factor, generates error SD
        #on Gaussian distribution. i.e. 6 cages with SD 1 will have 6 random error generated based on curve with SD 1.
        self.errorResults.clear()
        counts = len(s2inputs[1])
        result = []
        for i in range(counts):
            individualError = self.genOneEVal(int(s2inputs[1][i]),float(s3inputs[i+1]))
            result.append(individualError)
        self.errorResults = result


    def genOneEVal(self, count, sd):
        #Generates one error val
        lst = []
        for i in range(count):
            if sd != 0: #Handling case where SD is 0
                rand = random.uniform(0.0, 1.0)
                val = sc.norm(0, sd).ppf(rand)
                rounded = round(val, 4)
                lst.append(rounded)
            else: 
                lst.append(0)
        return lst
        



