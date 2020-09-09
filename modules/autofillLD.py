# Utilized for autofill of step 5 grid distribution... experimental and not quite as reliable as hand for small
# sample sizes or cartesian product.
# Check out this paper for more information: http://extremelearning.com.au/unreasonable-effectiveness-of-quasirandom-sequences/

# Copyright (C) 2020 Peyton Chen

import numpy as np

def phi(d):
    # Uses Newton-Rhapson-Method for phi calculation
    x=1.0000
    for i in range(100):
        x = x-(pow(x,d+1)-x-1)/((d+1)*pow(x,d)-1)
    return x


def runlowdiscseq(s1inputs):
    # Constructing quasi-random low discrepancy sequence to evenly distribute everything
    lst = []
    d = int(s1inputs[2]) + 1 #to account for treatments
    n = int(s1inputs[0]) #total measurements
    g = phi(d)
    alpha = np.zeros(d)                 
    s=0.5  # initial seed 0 is appparently ok but 0.5 works even better 

    for j in range(d):
        alpha[j] = pow(1/g,j+1) %1 #setting up alpha
    z = np.zeros((n, d))    
    for i in range(n):
        z = (s + alpha*(i+1)) %1 #setting up rest of low discrepancy sequence generation
        lst.append(z)
    return lst


def parsealgo(s1Inputs, s2Inputs, algoassign):
    # Parse results, calculate assignments, puts into dict to load in 
    dic = {}
    numT = int(s1Inputs[1])
    numBlst = s2Inputs[1]

    tassign = []
    for array in algoassign:
        val = array[0]
        if 0 <= val < (1/numT):
            tassign.append(1)
        else:
            i = 2 
            while (i/numT) <= 1:
                if ((i-1)/numT) <= val < (i/numT):
                    tassign.append(i)
                    break
                else:
                    i += 1

        for i in range(1, len(array)): #skipping treatment col since we already did that
            name = s2Inputs[0][i-1]
            bval = array[i]
            total = int(s2Inputs[1][i-1])

            if name not in dic: #creates new key, value if it doesn't exist
                dic[name] = []

            if 0 <= bval < (1/total):
                dic[name].append(1)
            else:
                i = 2 
                while (i/total) <= 1:
                    if ((i-1)/total) <= bval < (i/total):
                        dic[name].append(i)
                        break
                    else:
                        i += 1

    dic['Treatment'] = tassign
    return dic


def runLDalgo(s1Inputs, s2Inputs):
    lst = runlowdiscseq(s1Inputs)
    dic = parsealgo(s1Inputs, s2Inputs, lst)
    return dic