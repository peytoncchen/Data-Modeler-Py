#Input Object to store input data 

from PyQt5.QtWidgets import QLineEdit

class Inputs:
    def __init__(self):
        self.s1Inputs = []
        self.s2Obj = []
        self.s2Inputs = []
        self.s3Obj = []
        self.s3Inputs = []
        self.s4Obj = []
        self.s4Inputs = []
        self.s4labelobj = []
        self.s4labels = []
        self.s5Obj = []
        self.s5Inputs = []


    def store_s2(self, s2objlabel, s2objval):
        #Stores values from S2 into self var
        self.s2Inputs.clear()
        lstlabel = []
        lstval = []

        for obj in s2objlabel:
            lstlabel.append(str(obj.text()).strip())
        for obj in s2objval:
            lstval.append(str(obj.text()).strip())
        
        self.s2Inputs.append(lstlabel)
        self.s2Inputs.append(lstval)


    def store_s3and4(self, s3objval, s4objval, s4objlabel):
        #Stores values from S3 and S4 into self var
        self.s3Inputs.clear()
        self.s4Inputs.clear()
        self.s4labels.clear()

        lsts3 = []
        lsts4 = []
        lsts4label = []

        for obj in s3objval:
            lsts3.append(str(obj.text()).strip())
        
        for obj in s4objval:
            lsts4.append(str(obj.text()).strip())
        
        for obj in s4objlabel:
            lsts4label.append(str(obj.text()).strip())


        self.s3Inputs = lsts3
        self.s4Inputs = lsts4
        self.s4labels = lsts4label
        print(self.s4Inputs)
        print(self.s4labels)
    

    def stores_s5(self, s5objval):
        #Stores values from S5 into self var

        self.s5Inputs.clear()

        tLst = []
        bLst = []

        #Extract treatment assignments

        for obj in s5objval[0]:
            tLst.append(str(obj.text()).strip())
        
        #Extract blocking assignments
        for lst in s5objval[1]:
            iBlst = []
            for obj in lst:
                iBlst.append(str(obj.text()).strip())
            bLst.append(iBlst)
        
        self.s5Inputs.append(tLst)
        self.s5Inputs.append(bLst)


    def loadin_s5(self, s5objval, griddict):
        #Load in grid to Step 5 when load in csv grid option is chosen
        for i, obj in enumerate(s5objval[0]): #loading in treatments
            obj.setText(str(griddict['Treatment'][i]))

        keys = [*griddict] #Gets all the keys in griddict in list format
        keys.remove('Treatment') #Already taken care of loading in treatments
        
        for i, lst in enumerate(s5objval[1]):
            for key, obj in zip(keys, lst):
                obj.setText(str(griddict[key][i]))




        




    




    
    