#Input Object to store input data 

from PyQt5.QtWidgets import QLineEdit

class Inputs:
    def __init__(self, s1Inputs=None):
        self.s1Inputs = s1Inputs or []
        self.s2Obj = []
        self.s2Inputs = []

    def store_s2(self, s2objlabel, s2objval):
        lstlabel = []
        lstval = []

        for obj in s2objlabel:
            lstlabel.append(str(obj.text()))
        for obj in s2objval:
            lstval.append(str(obj.text()))
        
        self.s2Inputs.append(lstlabel)
        self.s2Inputs.append(lstval)




    
    