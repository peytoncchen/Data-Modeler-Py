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
        #tresult.result_frame.round(4)
        resultframe.append(tresult.result_frame)
        #resultframe.append(tresult.result_frame.loc[:,'pvalue-hs': 'reject-hs'])
    return resultframe


def todict(resultframe):
    dic = []
    for frame in resultframe:
        df = frame.loc[:,'pvalue-hs':'reject-hs']
        temp = df.to_dict()
        dic.append(temp)
    return dic
    
