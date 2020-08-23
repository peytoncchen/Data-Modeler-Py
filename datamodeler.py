# Data Modeler for Power Calculations Python Edition

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Mainwindow import Ui_MainWindow
from verify import s1verify
from inputs import Inputs


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.inputs = Inputs()

        self.bFbox = QFormLayout()
        self.bFscrollWidget.setLayout(self.bFbox)

        self.s1but.clicked.connect(self.s1process)
        

    def s1process(self):
        numM = str(self.numMeasure.text())
        numT = str(self.numTreat.text())
        numB = str(self.numBf.text())
        nameM = str(self.nameMeas.text())
        nameD = str(self.namedVar.text())
        self.inputs.s1Inputs = [numM, numT, numB, nameM, nameD]

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")
        if not s1verify(self.inputs.s1Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.clearLayout(self.bFbox)
            lstlabel = []
            lstval = []
            for i in range(int(numB)):
                bName = QLineEdit()
                bVal = QLineEdit()
                lstlabel.append(bName)
                lstval.append(bVal)
                self.bFbox.addRow(bName, bVal)
            self.inputs.s2Obj = []
            self.inputs.s2Obj.append(lstlabel)
            self.inputs.s2Obj.append(lstval)
    

    def s2process(self):
        pass

    
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
    window.resize(700, 300)
    window.show()

    sys.exit(app.exec_())
