import statsmodels.api as sm
import pandas as pd


def makedict(s5inputs, dVlist, s1inputs, s2inputs):
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
    result = s1inputs[4] + ' ~ ' + 'C(Treatment)'
    for name in s2inputs[0]:
        blkstring = ' + C(' + name + ')'
        result += blkstring
    return result


def makeglmresults(s5inputs, multiRun, s1inputs, s2inputs):
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
    keys = []
    for i in range(len(resultframe)):
        keys.append('Run ' + str(i + 1))
    return pd.concat(resultframe, keys=keys)


def todict(resultframe):
    dics = []
    for frame in resultframe:
        df = frame.loc[:,'pvalue-hs':'reject-hs']
        temp = df.to_dict()
        dics.append(temp)
    return dics


def parseddics(dics):  
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
