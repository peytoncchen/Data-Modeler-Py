import statsmodels.api as sm
import pandas as pd


def makedict(s5inputs, dVlist, s1inputs, s2inputs):
    #Makes a dict based on inputs to be used for data plugged into creating GLM
    result = {}
    result[s1inputs[4]] = dVlist
    result['Treatment'] = s5inputs[0]

    for i in range(len(s2inputs[0])):
        blk = []
        for lst in s5inputs[1]:
            blk.append(lst[i])
        result[s2inputs[0][i]] = blk

    return result


def makeformula(s1inputs, s2inputs):
    #Makes formula to be used with GLM
    result = s1inputs[4] + ' ~ ' + 'C(Treatment)'
    for name in s2inputs[0]:
        blkstring = ' + C(' + name + ')'
        result += blkstring
    return result


def makeglmresults(s5inputs, multiRun, s1inputs, s2inputs):
    #Runs GLM calculations, fits modle, runs pairwise t-test, extracts pandas dataframes rounded, stores into list
    formula = makeformula(s1inputs, s2inputs)
    resultframe = []
    for i in range(len(multiRun)):
        dic = makedict(s5inputs, multiRun[i], s1inputs, s2inputs)
        model = sm.GLM.from_formula(formula, dic)
        modelresult = model.fit()
        tresult = modelresult.t_test_pairwise('C(Treatment)')
        rounded = tresult.result_frame.round(4)
        resultframe.append(rounded)
    return resultframe


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
        label = 'For treatments ' + tdiff +', power estimation: ' + str(counter) + '/' + str(total) + ' or ' + str(rounded) + '%.'
        lstpwrlabels.append(label)
    return lstpwrlabels
