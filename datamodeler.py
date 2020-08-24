# Data Modeler for Power Calculations Python Edition

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Mainwindow import Ui_MainWindow
from verify import s1verify, s2verify, s3and4verify
from inputs import Inputs


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.inputs = Inputs()

        self.bFbox = QFormLayout()
        self.bFscrollWidget.setLayout(self.bFbox)

        self.tBox = QFormLayout()
        self.tScrollWidget.setLayout(self.tBox)

        self.eBox = QFormLayout()
        self.eRscrollWidget.setLayout(self.eBox)
        

        self.s1but.clicked.connect(self.s1process)
        self.s2but.clicked.connect(self.s2process)
        self.s4but.clicked.connect(self.s3and4process)
        self.pushButton.clicked.connect(self.test)
        

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
            print(self.inputs.s1Inputs)
            print(self.inputs.s2Inputs)
            print(self.inputs.s3Inputs)
            print(self.inputs.s4Inputs)


    def store_s1(self):
        numM = str(self.numMeasure.text())
        numT = str(self.numTreat.text())
        numB = str(self.numBf.text())
        nameM = str(self.nameMeas.text())
        nameD = str(self.namedVar.text())
        self.inputs.s1Inputs = [numM, numT, numB, nameM, nameD]

    
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
    

    def test(self):
        print(self.inputs.s3Obj)
        print(self.inputs.s4Obj)



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
