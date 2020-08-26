# Data Modeler for Power Calculations Python Edition

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Mainwindow import Ui_MainWindow
from verify import s1verify, s2verify, s3and4verify, s5verify
from inputs import Inputs
from results import Results


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.inputs = Inputs()
        self.results = Results()

        self.bFbox = QFormLayout()
        self.bFscrollWidget.setLayout(self.bFbox)

        self.tBox = QFormLayout()
        self.tScrollWidget.setLayout(self.tBox)

        self.eBox = QFormLayout()
        self.eRscrollWidget.setLayout(self.eBox)

        self.dGrid = QGridLayout()
        self.dScrollWidget.setLayout(self.dGrid)

        self.dGroupBox.hide()
        self.cGroupBox.hide()

        self.setMinimumSize(QSize(450, 750))
        self.resize(450, 750)

        self.s1but.clicked.connect(self.s1process)
        self.s2but.clicked.connect(self.s2process)
        self.s4but.clicked.connect(self.s3and4process)
        self.s5but.clicked.connect(self.s5process)
    

    def s5update(self):
        self.inputs.stores_s5(self.inputs.s5Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")
        if not s5verify(self.inputs.s5Inputs, self.inputs.s1Inputs, self.inputs.s2Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            print(self.inputs.s5Inputs)
            self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
            print(self.results.dVResults)
            self.updatedVVal()
            

    def s5process(self):
        self.inputs.stores_s5(self.inputs.s5Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")
        if not s5verify(self.inputs.s5Inputs, self.inputs.s1Inputs, self.inputs.s2Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            print(self.inputs.s5Inputs)
            self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
            print(self.results.dVResults)
            self.initdVValView()
            self.s5but.clicked.disconnect(self.s5process)
            self.s5but.clicked.connect(self.s5update)            


    def expand(self):
        self.setMinimumSize(QSize(900, 750))
        self.resize(900, 750)
        self.dGroupBox.show()
        self.cGroupBox.show()
        

    def s1process(self):
        self.store_s1()

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")
        if not s1verify(self.inputs.s1Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.initBfView()
            self.initTView() 
            if int(self.inputs.s1Inputs[2]) == 0:
                pass
                #fix right now index error self.initEView() 
    

    def s2process(self):
        self.inputs.store_s2(self.inputs.s2Obj[0], self.inputs.s2Obj[1])

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")
        if not s2verify(self.inputs.s2Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.initEView()
    

    def s3and4process(self):
        self.inputs.store_s3and4(self.inputs.s3Obj, self.inputs.s4Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        if not s3and4verify(self.inputs.s3Inputs, self.inputs.s4Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.expand()
            self.initDView()
            self.results.genEVals(self.inputs.s2Inputs, self.inputs.s3Inputs)
            print(self.results.errorResults)


    def store_s1(self):
        numM = str(self.numMeasure.text())
        numT = str(self.numTreat.text())
        numB = str(self.numBf.text())
        nameM = str(self.nameMeas.text())
        nameD = str(self.namedVar.text())
        self.inputs.s1Inputs = [numM, numT, numB, nameM, nameD]


    def updatedVVal(self):
        self.name.setText(self.inputs.s1Inputs[4])
        self.name.repaint()

        for i in range(len(self.results.dVResults)):
            self.results.dVObjects[i].setText(str(self.results.dVResults[i]))
            self.results.dVObjects[i].repaint()
            

    def initdVValView(self):
        labellst = []
        colCount = int(self.inputs.s1Inputs[2]) + 2
        self.name = QLabel(self.inputs.s1Inputs[4])
        self.name.setAlignment(Qt.AlignHCenter)
        self.name.setFixedHeight(21)
        self.dGrid.addWidget(self.name,0,colCount)
        for i in range(len(self.results.dVResults)):
            label = QLabel(str(self.results.dVResults[i]))
            label.setAlignment(Qt.AlignHCenter)
            label.setFixedHeight(21)
            labellst.append(label)
            self.dGrid.addWidget(label,i+1,colCount)
        self.results.dVObjects = labellst
    
    
    def initDView(self):
        self.clearLayout(self.dGrid)
        tAssignObj = []
        bAssignObj = []

        #Init the row labels
        l1 = QLabel(self.inputs.s1Inputs[3])
        l2 = QLabel("Treatment")
        l1.setAlignment(Qt.AlignHCenter)
        l2.setAlignment(Qt.AlignHCenter)
        l1.setFixedHeight(21)
        l2.setFixedHeight(21)
        self.dGrid.addWidget(l1,0,0)
        self.dGrid.addWidget(l2,0,1)

        for i in range(len(self.inputs.s2Inputs[0])):
            blabel = QLabel(self.inputs.s2Inputs[0][i])
            blabel.setFixedHeight(21)
            blabel.setAlignment(Qt.AlignHCenter)
            self.dGrid.addWidget(blabel,0,i+2)

        #Init the rest of distribute groups view
        for i in range(int(self.inputs.s1Inputs[0])):
            numl = QLabel(str(i+1))
            numl.setMaximumWidth(125)
            numl.setAlignment(Qt.AlignHCenter)
            self.dGrid.addWidget(numl,i+1,0)
            tAssign = QLineEdit()
            tAssign.setFixedHeight(21)
            tAssign.setMaximumWidth(125)
            tAssign.setAlignment(Qt.AlignHCenter)
            tAssignObj.append(tAssign)
            self.dGrid.addWidget(tAssign,i+1,1)

            iBAssign = []
            for j in range(len(self.inputs.s2Inputs[0])):
                bAssign = QLineEdit()
                bAssign.setFixedHeight(21)
                bAssign.setMaximumWidth(125)
                bAssign.setAlignment(Qt.AlignHCenter)
                iBAssign.append(bAssign)
                self.dGrid.addWidget(bAssign,i+1,j+2)
            bAssignObj.append(iBAssign)

        self.inputs.s5Obj.clear()
        self.inputs.s5Obj.append(tAssignObj)
        self.inputs.s5Obj.append(bAssignObj)

    
    def initEView(self):
        self.clearLayout(self.eBox)
        lsterrors = []

        totalerror = QLabel("Total error SD:")
        totalerrorval = QLineEdit()
        self.eBox.addRow(totalerror, totalerrorval)
        lsterrors.append(totalerrorval)

        for i in range(len(self.inputs.s2Inputs[0])):
            label = QLabel(self.inputs.s2Inputs[0][i] + ' SD:')
            sdval = QLineEdit()
            lsterrors.append(sdval)
            self.eBox.addRow(label, sdval)
        self.inputs.s3Obj.clear()
        self.inputs.s3Obj = lsterrors


    def initTView(self):
        self.clearLayout(self.tBox)
        lstmeans = []
        for i in range(int(self.inputs.s1Inputs[1])):
            num = QLabel(str(i + 1))
            mean = QLineEdit()
            lstmeans.append(mean)
            self.tBox.addRow(num, mean)
        self.inputs.s4Obj.clear()
        self.inputs.s4Obj = lstmeans


    def initBfView(self):
        self.clearLayout(self.bFbox)
        lstlabel = []
        lstval = []
        for i in range(int(self.inputs.s1Inputs[2])):
            bName = QLineEdit()
            bVal = QLineEdit()
            lstlabel.append(bName)
            lstval.append(bVal)
            self.bFbox.addRow(bName, bVal)
        self.inputs.s2Obj.clear()
        self.inputs.s2Obj.append(lstlabel)
        self.inputs.s2Obj.append(lstval)


    def clearLayout(self, layout):
        while layout.count():
            c = layout.takeAt(0)
            if c.widget() is not None:
                c.widget().deleteLater()
            elif c.layout() is not None:
                clearLayout(c.layout())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
