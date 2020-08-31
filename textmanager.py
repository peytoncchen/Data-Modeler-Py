#Prepares text file strings

def preparelabeltxt(s1inputs, s2inputs):
    #Generates label text for non-SAS output
        labels = []
        labels.append(s1inputs[3])
        labels.append('Treatment')

        for name in s2inputs[0]:
            labels.append(name)
    
        labels.append(s1inputs[4])

        return labels


def preparemultisas(s5inputs, multiRun, s1inputs, s2inputs, eName):
    #Generates string to be outputted into SAS script file
    #Prepares all labels by removing all spaces
    expmtName = eName.replace(' ', '')
    nmMeas = s1inputs[3].replace(' ', '')
    dvNm = s1inputs[4].replace(' ', '')

    blocklist = [label.replace(' ', '') for label in s2inputs[0]]

    bigboysas = ''
    blockName = ' '.join(blocklist)
    sasstart = 'DATA ' + expmtName + '; INPUT ' + nmMeas + ' Treatment ' + blockName + ' ' + dvNm + '; Lines;\n\n'
    sasfinish = '\n;\nRUN;\n\nPROC MIXED ASYCOV NOBOUND DATA=' + expmtName + ' ALPHA=0.05;\nCLASS Treatment ' + blockName + ';\n'
    sasfinish += 'MODEL ' + dvNm + ' = ' + 'Treatment ' + blockName + '\n'
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
    #Prepares text file non-SAS information for multiple runs
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
    #Prepares text for one set of dVResults
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
        tempstr = ' '.join(lst)
        tempstr += '\n'
        string += tempstr

    return string




