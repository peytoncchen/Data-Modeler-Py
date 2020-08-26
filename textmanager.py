#Prepares text file strings

def preparemultitxt(s5inputs, multiRun, s1inputs, s2inputs):
    bigboystring = ''
    for lst in multiRun:
        tempstr = preparetxt(s5inputs, lst, s1inputs, s2inputs)
        tempstr += '\n\n\n'
        bigboystring += tempstr
    return bigboystring




def preparetxt(s5inputs, dVResults, s1inputs, s2inputs):
    string = ''

    result = []
    labels = []
    labels.append(s1inputs[3])
    labels.append('Treatment')

    for name in s2inputs[0]:
        labels.append(name)
    
    labels.append(s1inputs[4])
    result.append(labels)


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



