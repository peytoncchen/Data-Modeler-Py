#Input Object to store input data 

from PyQt5.QtWidgets import QLineEdit

class Inputs:
    def __init__(self, s1Inputs=None, s2Obj=None, s2Inputs=None, s3Obj=None, s3Inputs=None, s4Obj=None, s4Inputs=None):
        self.s1Inputs = s1Inputs or []
        self.s2Obj = s2Obj or []
        self.s2Inputs = s2Inputs or []
        self.s3Obj = s3Obj or []
        self.s3Inputs = s3Inputs or []
        self.s4Obj = s4Obj or []
        self.s4Inputs = s4Inputs or []


    def store_s2(self, s2objlabel, s2objval):
        self.s2Inputs.clear()
        lstlabel = []
        lstval = []

        for obj in s2objlabel:
            lstlabel.append(str(obj.text()))
        for obj in s2objval:
            lstval.append(str(obj.text()))
        
        self.s2Inputs.append(lstlabel)
        self.s2Inputs.append(lstval)


    def store_s3and4(self, s3objval, s4objval):
        self.s3Inputs.clear()
        self.s4Inputs.clear()

        lst1 = []
        lst2 = []

        for obj in s3objval:
            lst1.append(str(obj.text()))
        
        for obj in s4objval:
            lst2.append(str(obj.text()))

        self.s3Inputs = lst1
        self.s4Inputs = lst2
    




    
    