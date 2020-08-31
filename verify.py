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
        return False, 'Invalid input - integer input expected'

    if int(numM) < 0 or int(numT) < 0 or int(numB) < 0:
        return False, 'Invalid input - integers must be positive'
    
    if int(numT) < 2:
        return False, 'Invalid input - must have at least 2 treatments'

    
    if nameM == '' or namedVar == '':
        return False, 'Invalid input - name measurements and name of dependent variable cannot be blank'
    
    return True, ''


# 2 lists one with labels, the other with values example -> [['Rat', 'Cage', 'Gender'], ['1', '2', '3']]
def s2verify(s2list):
    names = s2list[0]
    values = s2list[1]

    for name in names:
        if name == '':
            return False, 'Invalid input - blocking factor names cannot be blank'
    
    for value in values:
        try:
            int(value)
        except ValueError:
            return False, 'Invalid input - integer input expected for blocking factor values'
        if int(value) < 0:
            return False, 'Invalid input - integers must be positive'
    
    return True, ''


def s3and4verify(s3list, s4list):
    for val in s3list:
        try:
            float(val)
        except ValueError:
            return False, 'Invalid input - float input expected for SD'
        if float(val) < 0:
            return False, 'Invalid input - SD must be positive'
    
    for val in s4list:
        try:
            float(val)
        except ValueError:
            return False, 'Invalid input - float input expected for treatment means'
    
    return True, ''

#2 lists one that stores treatment assignment, then a list of a list of blocking factor assignments
#-> [[1,2,3,4],[[1,2][1,2],[2,1],[2,1]]]
def s5verify(s5list, s1inputs, s2inputs):
    tRange = int(s1inputs[1])

    for num in s5list[0]:
        try:
            int(num)
        except ValueError:
            return False, 'Invalid input - treatment assignment numbers must be integers'
        
        if int(num) not in range(1, tRange+1):
            return False, 'Invalid input - treatment assignment number out of range'
    

    for lst in s5list[1]:
        for i in range(len(lst)):
            try:
                int(lst[i])
            except ValueError:
                return False, 'Invalid input - blocking factor assignment numbers must be integers'
            
            if int(lst[i]) not in range(1, int(s2inputs[1][i]) + 1):
                return False, 'Invalid input - blocking factor assignment number out of range'
    
    return True, ''



    
    
