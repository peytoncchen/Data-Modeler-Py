#Contains functions necssary for GLM output and analysis 

# Copyright (C) 2020 Peyton Chen

import statsmodels.api as sm
import pandas as pd
from scipy import stats
import copy


def makedict(s5inputs, dVlist, s1inputs, s2inputs, big):
    #Makes a dict based on inputs to be used for data plugged into creating GLM
    result = {}
    result[s1inputs[4].replace(' ', '')] = dVlist
    if big:
        result['Treatment'] = s5inputs[0]

    for i in range(len(s2inputs[0])):
        blk = []
        for lst in s5inputs[1]:
            blk.append(lst[i])
        result[s2inputs[0][i].replace(' ', '')] = blk

    return result


def makeformula(s1inputs, s2inputs, big):
    #Makes formula to be used with GLM
    result = s1inputs[4].replace(' ', '') + ' ~ '
    if big:
        result += 'C(Treatment) + '
    for name in s2inputs[0]:
        blkstring = 'C(' + name.replace(' ', '') + ') + '
        result += blkstring
    return result[:-3] #accounting for superfluous + character at the end of the formula


def calcnestedfstat(smallmodel, bigmodel):
    #Given two fitted GLMs, the larger of which contains treatment compared to smaller, 
    #returns the f-stat and p-value corresponding to the larger model adding explanatory power
    addtlparams = bigmodel.df_model - smallmodel.df_model
    fstat = (smallmodel.deviance - bigmodel.deviance) / (addtlparams * bigmodel.scale)
    dfnumerator = addtlparams
    # use fitted values to obtain n_obs from model object:
    dfdenom = (bigmodel.fittedvalues.shape[0] - bigmodel.df_model)
    pvalue = stats.f.sf(fstat, dfnumerator, dfdenom)
    return fstat, pvalue


def makeglmresults(s5inputs, multiRun, s1inputs, s2inputs):
    #Runs GLM calculations, fits model, runs pairwise t-test, extracts pandas dataframes rounded, stores into list
    formula = makeformula(s1inputs, s2inputs, True)
    resultframe = []
    bigmodels = []
    for i in range(len(multiRun)):
        dic = makedict(s5inputs, multiRun[i], s1inputs, s2inputs, True)
        model = sm.GLM.from_formula(formula, dic)
        modelresult = model.fit()
        bigmodels.append(modelresult)
        tresult = modelresult.t_test_pairwise('C(Treatment)')
        rounded = tresult.result_frame.round(4)
        resultframe.append(rounded)
    return resultframe, bigmodels


def makeftest(s5inputs, multiRun, s1inputs, s2inputs, bigmodels):
    #Based on GLMs, makes f-test and outputs list of tuples of fstat, p-value for each run
    formula = makeformula(s1inputs, s2inputs, False)
    results = []
    for i in range(len(multiRun)):
        dic = makedict(s5inputs, multiRun[i], s1inputs, s2inputs, False)
        smallmodel = sm.GLM.from_formula(formula, dic).fit()
        tup = calcnestedfstat(smallmodel, bigmodels[i])
        results.append(tup)
    return results


def exportresultframe(resultframe):
    #Prepares all dataframees to be extracted and exported 
    keys = []
    for i in range(len(resultframe)):
        keys.append('Run ' + str(i + 1))
    return pd.concat(resultframe, keys=keys)


def todict(resultframe):
    #Takes t-test pairwise resultframes and extracts them into dicts for power estimations
    dics = []
    for frame in resultframe:
        df = frame.loc[:,'pvalue-hs':'reject-hs']
        temp = df.to_dict()
        dics.append(temp)
    return dics


def parseddics(dics):
    #Reorganizes dicts to have all treatments' bool contained together  
    result = {}
    if dics:
        combokeys = dics[0]['reject-hs'].keys()
        result = {}
        for key in combokeys:
            lst = []
            for dic in dics:
                 lst.append(dic['reject-hs'][key])
            result[key] = lst
    return result


def printpwr(resultframe):
    #Produces labels to be displayed pwr estimation view box.
    dics = todict(resultframe)
    parsed = parseddics(dics)
    lstpwrlabels = []

    for tdiff in parsed:
        total = len(parsed[tdiff])
        counter = 0
        for val in parsed[tdiff]:
            if val:
                counter += 1
        pwr = (counter/total) * 100
        rounded = round(pwr, 1)
        label = '  For treatments ' + tdiff +', power estimation: ' + str(counter) + '/' + str(total) + ' or ' + str(rounded) + '%.'
        lstpwrlabels.append(label)
    return lstpwrlabels


def fpwr(fresults):
    #Produces label to displayed for fixed effect pwr estimation view box.
    counter = 0
    total = len(fresults)
    for result in fresults:
        if result[1] < 0.05:
            counter += 1
    percentage = round((counter/total)*100, 1)
    label = '  Overall effect of treatment has estimated power: ' + str(counter) + '/' + str(total) + ' or ' + str(percentage) + '%.'

    return label
