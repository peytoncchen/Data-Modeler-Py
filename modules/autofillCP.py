# Homebrew autofill feature for lower sample sizes utilizing cartesian products for full factorial design

# Copyright (C) 2020 Peyton Chen

import itertools #for itertools.product


def preparearray(s1inputs, s2inputs):
    #Prepares array based on inputs to find cartesian product
    result = []
    tlst = [i+1 for i in range(int(s1inputs[1]))]
    result.append(tlst)

    for blkfc in s2inputs[1]:
        blklst = [i+1 for i in range(int(blkfc))]
        result.append(blklst)
    
    return result


def combotodict(combos, s2inputs):
    #Takes combos and turns it into a dict to load in
    dic = {}
    for combo in combos:
        if 'Treatment' not in dic:
            dic['Treatment'] = []
        dic['Treatment'].append(combo[0])

        for i, bkfc in enumerate(s2inputs[0]):
            if bkfc not in dic:
                dic[bkfc] = []
            dic[bkfc].append(combo[i + 1])
    return dic


def runCPalgo(s1inputs, s2inputs):
    start = preparearray(s1inputs, s2inputs)
    combos = [p for p in itertools.product(*start)]
    return combos


def verifyCPalgo(s1inputs, combos):
    if int(s1inputs[0]) % len(combos) != 0:
        return False, "Consider adding more measurements so that you reach a multiple of " + str(len(combos)) + " for complete factorial design"
    else:
        return True, ''


def combotofitgrid(combos, s2inputs, s1inputs):
    #Fits combos to grid incase there needs to be doubling/tripling up, etc.
    n = int(s1inputs[0]) // len(combos)
    if n > 1:
        newcombos = [item for item in combos for _ in range(n)]
        return combotodict(newcombos, s2inputs)
    else:
        return combotodict(combos, s2inputs)
        

    




