#Results object to store generated results from calculations 

import random
import scipy.stats as sc


class Results:
    def __init__(self, errorResults=None, dVObjects=None, dVResults=None):
        self.errorResults = errorResults or []
        self.dVObjects = dVObjects or []
        self.dVResults = dVResults or []


    def gendvVals(self, s5inputs, s4inputs, totalerror):
        self.dVResults.clear()
        count = len(s5inputs[0])
        numBF = len(s5inputs[1][0])
        result = []
        for i in range(count):
            dvVal = 0.0
            tNum = int(s5inputs[0][i])
            dvVal += float(s4inputs[tNum-1]) #adding treatment value

            rand = random.uniform(0.0, 1.0)
            tEVal = sc.norm(0, float(totalerror)).ppf(rand)
            dvVal += tEVal #adding generated total error value based on totalerror SD value

            for j in range(numBF):
                bFnum = int(s5inputs[1][i][j])
                dvVal += self.errorResults[j][bFnum-1]
            
            rounded = round(dvVal, 4)
            result.append(rounded)
        
        self.dVResults = result


    def genEVals(self, s2inputs, s3inputs):
        self.errorResults.clear()
        counts = len(s2inputs[1])
        result = []
        for i in range(counts):
            individualError = self.genOneEVal(int(s2inputs[1][i]),float(s3inputs[i+1]))
            result.append(individualError)
        self.errorResults = result


    def genOneEVal(self, count, sd):
        lst = []
        for i in range(count):
            rand = random.uniform(0.0, 1.0)
            val = sc.norm(0, sd).ppf(rand)
            rounded = round(val, 4)
            lst.append(rounded)
        return lst
        



