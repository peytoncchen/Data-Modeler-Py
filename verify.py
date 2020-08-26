#Verifying all the inputs at each step

def s1verify(s1list):
    numM = s1list[0]
    numT = s1list[1]
    numB = s1list[2]
    nameM = s1list[3]
    namedVar = s1list[4]

    try:
        int(numM)
        int(numT)
        int(numB)
    except ValueError:
        return False

    if ' ' in nameM or ' ' in namedVar:
        return False
    
    if nameM == '' or namedVar == '':
        return False
    
    return True


# 2 lists one with labels, the other with values example -> [['Rat', 'Cage', 'Gender'], ['1', '2', '3']]
def s2verify(s2list):
    names = s2list[0]
    values = s2list[1]

    for name in names:
        if ' ' in name:
            return False
        if name == '':
            return False
    
    for value in values:
        try:
            int(value)
        except ValueError:
            return False
    
    return True


def s3and4verify(s3list, s4list):
    for val in s3list:
        try:
            float(val)
        except ValueError:
            return False
    
    for val in s4list:
        try:
            float(val)
        except ValueError:
            return False
    
    return True


def s5verify(s5list, s1inputs, s2inputs):
    tRange = int(s1inputs[1])

    for num in s5list[0]:
        try:
            int(num)
        except ValueError:
            return False
        
        if int(num) not in range(1, tRange+1):
            return False
    

    for lst in s5list[1]:
        for i in range(len(lst)):
            try:
                int(lst[i])
            except ValueError:
                return False
            
            if int(lst[i]) not in range(1, int(s2inputs[1][i]) + 1):
                return False
    
    return True



    
    
