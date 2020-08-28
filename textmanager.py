#Prepares text file strings

def preparelabeltxt(s1inputs, s2inputs):
        labels = []
        labels.append(s1inputs[3])
        labels.append('Treatment')

        for name in s2inputs[0]:
            labels.append(name)
    
        labels.append(s1inputs[4])

        return labels


def preparemultisas(s5inputs, multiRun, s1inputs, s2inputs, eName):
    bigboysas = ''
    blockName = ' '.join(s2inputs[0])
    sasstart = 'DATA ' + eName + '; INPUT ' + s1inputs[3] + ' Treatment ' + blockName + ' ' + s1inputs[4] + '; Lines;\n\n'
    sasfinish = '\n;\nRUN;\n\nPROC MIXED ASYCOV NOBOUND DATA=' + eName + ' ALPHA=0.05;\nCLASS Treatment ' + blockName + ';\n'
    sasfinish += 'MODEL ' + s1inputs[4] + ' = ' + 'Treatment ' + blockName + '\n'
    sasfinish += '/SOLUTION DDFM=KENWARDROGER;\nlsmeans Treatment / adjust=tukey;\nRUN;\n\n\n'
    

    for lst in multiRun:
        string = ''
        string += sasstart
        tempstr = preparetxt(s5inputs, lst, s1inputs, s2inputs)
        string += tempstr
        string += sasfinish
        bigboysas += string
    return bigboysas



def preparemultitxt(s5inputs, multiRun, s1inputs, s2inputs):
    bigboystring = ''
    lstheader = []
    labels = preparelabeltxt(s1inputs, s2inputs)
    lstheader.append(labels)
    for label in lstheader:
        header = ','.join(label)
        header += '\n\n'
        bigboystring += header

    for lst in multiRun:
        tempstr = preparetxt(s5inputs, lst, s1inputs, s2inputs)
        tempstr += '\n\n'
        bigboystring += tempstr
    return bigboystring




def preparetxt(s5inputs, dVResults, s1inputs, s2inputs):
    string = ''

    result = []

    for i in range(len(s5inputs[0])):
        temp = []
        temp.append(str(i+1))
        temp.append(s5inputs[0][i])

        for j in range(len(s5inputs[1][i])):
            temp.append(s5inputs[1][i][j])

        temp.append(str(dVResults[i]))
        result.append(temp)
    
    for lst in result:
        tempstr = ','.join(lst)
        tempstr += '\n'
        string += tempstr

    return string




