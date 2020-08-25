#Input Object to store input data 

from PyQt5.QtWidgets import QLineEdit

class Inputs:
    def __init__(self, s1Inputs=None, s2Obj=None, s2Inputs=None, s3Obj=None, s3Inputs=None, 
    s4Obj=None, s4Inputs=None, s5Obj=None, s5Inputs=None):
        self.s1Inputs = s1Inputs or []
        self.s2Obj = s2Obj or []
        self.s2Inputs = s2Inputs or []
        self.s3Obj = s3Obj or []
        self.s3Inputs = s3Inputs or []
        self.s4Obj = s4Obj or []
        self.s4Inputs = s4Inputs or []
        self.s5Obj = s5Obj or []
        self.s5Inputs = s5Inputs or []


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

        lsts3 = []
        lsts4 = []

        for obj in s3objval:
            lsts3.append(str(obj.text()))
        
        for obj in s4objval:
            lsts4.append(str(obj.text()))

        self.s3Inputs = lsts3
        self.s4Inputs = lsts4
    

    def stores_s5(self, s5objval):
        self.s5Inputs.clear()

        tLst = []
        bLst = []

        #Extract treatment assignments

        for obj in s5objval[0]:
            tLst.append(str(obj.text()))
        
        #Extract blocking assignments
        for lst in s5objval[1]:
            iBlst = []
            for obj in lst:
                iBlst.append(str(obj.text()))
            bLst.append(iBlst)
        
        self.s5Inputs.append(tLst)
        self.s5Inputs.append(bLst)


    




    
    