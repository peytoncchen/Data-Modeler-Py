# Data Modeler for Power Calculations Python Edition

import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Mainwindow import Ui_MainWindow
from verify import s1verify, s2verify, s3and4verify, s5verify
from textmanager import preparemultitxt, preparemultisas
from generateglm import makeglmresults, printpwr, exportresultframe
from inputs import Inputs
from results import Results
from displaypd import pandasModel


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.inputs = Inputs()
        self.results = Results()

        self.runcounter = 0

        self.bFbox = QFormLayout()
        self.bFscrollWidget.setLayout(self.bFbox)

        self.cBox = QHBoxLayout()
        self.cScrollWidget.setLayout(self.cBox)

        self.tBox = QFormLayout()
        self.tScrollWidget.setLayout(self.tBox)

        self.eBox = QFormLayout()
        self.eRscrollWidget.setLayout(self.eBox)

        self.dGrid = QGridLayout()
        self.dScrollWidget.setLayout(self.dGrid)

        self.dfBox = QVBoxLayout()
        self.GLMScrollWidget.setLayout(self.dfBox)

        self.pwrBox = QVBoxLayout()
        self.PCScrollWidget.setLayout(self.pwrBox)

        self.dGroupBox.hide()
        self.cGroupBox.hide()
        self.GLMGroupBox.hide()
        self.PCGroupBox.hide()
        self.s2but.hide()
        self.updates4.hide()
        self.hides6fields()

        self.setMinimumSize(QSize(450, 750))
        self.resize(450, 750)

        self.updatebool = False
        self.initbool = True

        self.s1but.clicked.connect(self.s1process)
        self.s2but.clicked.connect(self.s2process)
        self.s4but.clicked.connect(self.s3and4process)
        self.updates4.clicked.connect(self.s3and4update)
        self.s5but.clicked.connect(self.s5process)
        self.addRun.clicked.connect(self.s5add)
        self.exportTxt.clicked.connect(self.exporttxt)
        self.exportSAS.clicked.connect(self.exportsas)
        self.glmCalc.clicked.connect(self.runglm)
        self.parsepower.clicked.connect(self.pwr)
        self.exportpwrcsv.clicked.connect(self.exportframes)

    
    def exportframes(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dataframe = exportresultframe(self.results.resultframes)
        if dlg.exec_():
            dir = dlg.getSaveFileName()
            dataframe.to_csv(str(dir[0]) + '.csv', index=True)


    def pwr(self):
        self.clearLayout(self.pwrBox)
        labels = printpwr(self.results.resultframes)
        headpwrlabel = QLabel('Based on ' + str(len(self.results.multiRun)) + ' runs and alpha = 0.05, power is estimated for difference between means:')
        self.pwrBox.addWidget(headpwrlabel)
        for label in labels:
            self.pwrBox.addWidget(QLabel(label))

    
    def runglm(self):
        self.expand2()
        self.clearLayout(self.dfBox)
        resultframes = makeglmresults(self.inputs.s5Inputs, self.results.multiRun, self.inputs.s1Inputs, self.inputs.s2Inputs)
        self.results.resultframes.clear()
        self.results.resultframes = resultframes

        for frame in self.results.resultframes:
            model = pandasModel(frame)
            view = QTableView()
            view.setModel(model)

            #setting height of TableViews, capping expandability @ 4 treatments / 6 rows
            height = view.rowHeight(0)
            numRows = model.rowCount()
            if numRows > 6:
                numRows = 6
            height = (height * numRows) 

            view.resizeColumnsToContents()
            view.resizeRowsToContents()
            view.setMinimumHeight(height)
            self.dfBox.addWidget(view)

    
    def hides6fields(self):
        self.addRun.hide()
        self.runCount.hide()
        self.exportTxt.hide()
        self.label.hide()
        self.experimentName.hide()
        self.exportSAS.hide()
        self.glmCalc.hide()
    

    def shows6fields(self):
        self.addRun.show()
        self.addRun.repaint()
        self.runCount.show()
        self.runCount.repaint()
        self.exportTxt.show()
        self.exportTxt.repaint()
        self.label.show()
        self.label.repaint()
        self.experimentName.show()
        self.experimentName.repaint()
        self.exportSAS.show()
        self.exportSAS.repaint()
        self.glmCalc.show()
        self.glmCalc.repaint()


    
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
            self.s1but.setText('Update')
            self.s1but.repaint()
            if int(self.inputs.s1Inputs[2]) == 0:
                self.initEView(True) 
                self.s2but.hide()
                self.resize(451,750)
                self.resize(450,750)
                self.inputs.s2Inputs.append([])
                self.inputs.s2Inputs.append([])
            else:
                self.s2but.show()
                self.s2but.repaint()
    

    def s2process(self):
        self.inputs.store_s2(self.inputs.s2Obj[0], self.inputs.s2Obj[1])

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")
        if not s2verify(self.inputs.s2Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.initEView(False)
            self.s2but.setText('Update')
            self.s2but.repaint()
    

    def s3and4update(self):
        self.inputs.store_s3and4(self.inputs.s3Obj, self.inputs.s4Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        if not s3and4verify(self.inputs.s3Inputs, self.inputs.s4Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.results.genEVals(self.inputs.s2Inputs, self.inputs.s3Inputs)
            self.results.cleardVResultView()
            self.results.multiRun.clear()
            self.s5but.setText('Generate values')
            self.s5but.repaint()
            self.updatedVVal()
            self.initcurrInpView()
            self.updatebool = True
            self.hides6fields()


    def s3and4process(self):
        self.inputs.store_s3and4(self.inputs.s3Obj, self.inputs.s4Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        if not s3and4verify(self.inputs.s3Inputs, self.inputs.s4Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.s4but.setText('Reset Grid')
            self.s4but.repaint()
            self.s5but.setText('Generate values')
            self.s5but.repaint()
            self.expand() #glitchy with expand2 
            self.initDView()
            self.results.genEVals(self.inputs.s2Inputs, self.inputs.s3Inputs)
            self.initcurrInpView()
            self.updatebool = False
            self.hides6fields()


    def s5process(self):
        self.inputs.stores_s5(self.inputs.s5Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")
        if not s5verify(self.inputs.s5Inputs, self.inputs.s1Inputs, self.inputs.s2Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
            self.results.multiRun.clear()
            self.results.addRun()
            self.runcounter = 1
            self.runCount.setText('Current run count: ' + str(self.runcounter))
            if not self.updatebool:
                self.initdVValView()
                self.s5but.setText('Reset runs')
                self.s5but.repaint()
                self.updates4.show()
                self.updates4.repaint()
                self.shows6fields()
                self.updatebool = True
            else:
                self.shows6fields()
                self.updatedVVal()
                self.runCount.repaint()
                self.updatebool = True    


    def s5add(self):
        self.inputs.stores_s5(self.inputs.s5Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")
        if not s5verify(self.inputs.s5Inputs, self.inputs.s1Inputs, self.inputs.s2Inputs):
            self.statusBar.showMessage('Invalid Input')
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
            self.runcounter += 1
            self.runCount.setText('Current run count: ' + str(self.runcounter))
            self.runCount.repaint()
            self.updatedVVal()
            self.results.addRun()


    def exporttxt(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        outstring = preparemultitxt(self.inputs.s5Inputs, self.results.multiRun, self.inputs.s1Inputs, self.inputs.s2Inputs)
        if dlg.exec_():
            dir = dlg.getSaveFileName()
            f = open(str(dir[0]) + '.txt', 'w+')
            f.write(outstring)
            f.close()


    def exportsas(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if self.experimentName.text() == '':
            self.experimentName.setText('UnnamedExpmt')
            self.experimentName.repaint()
        outstring = preparemultisas(self.inputs.s5Inputs, self.results.multiRun, self.inputs.s1Inputs, 
        self.inputs.s2Inputs, self.experimentName.text())
        if dlg.exec_():
            dir = dlg.getSaveFileName()
            f = open(str(dir[0]) + '.txt', 'w+')
            f.write(outstring)
            f.close()
                  

    def initcurrInpView(self):
        self.clearLayout(self.cBox)
        self.errors = QLabel()
        self.tmeans = QLabel()
        self.errors.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.errors.setCursor(Qt.IBeamCursor)
        self.tmeans.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.tmeans.setCursor(Qt.IBeamCursor)
        self.errors.setAlignment(Qt.AlignTop)
        self.tmeans.setAlignment(Qt.AlignTop)
        self.cBox.addWidget(self.errors)
        self.cBox.addWidget(self.tmeans)

        generrors = ''
        tmeans = 'Treatment Means:\n'

        for i in range(len(self.inputs.s2Inputs[0])):
            generrors += self.inputs.s2Inputs[0][i] + ' SD generated error:\n'
            for j in range(len(self.results.errorResults[i])):
                generrors += str(j + 1)
                generrors += ': '
                generrors += str(self.results.errorResults[i][j])
                generrors += '\n'
            generrors += '\n'

        for i in range(len(self.inputs.s4Inputs)):
            tmeans += str(i + 1)
            tmeans += ': '
            tmeans += self.inputs.s4Inputs[i]
            tmeans += '\n'  
        
        if generrors == '':
            generrors = 'No SD generated errors'

        self.errors.setText(generrors)
        self.tmeans.setText(tmeans)      
        self.errors.repaint()
        self.tmeans.repaint()



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
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            label.setCursor(Qt.IBeamCursor)
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

    
    def initEView(self,emptybool):
        self.clearLayout(self.eBox)
        lsterrors = []

        totalerror = QLabel("Total error SD:")
        totalerrorval = QLineEdit()
        self.eBox.addRow(totalerror, totalerrorval)
        lsterrors.append(totalerrorval)

        if not emptybool:
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


    def expand2(self):
        self.setMinimumSize(QSize(1350, 750))
        self.resize(1350, 750)
        self.GLMGroupBox.show()
        self.PCGroupBox.show()


    def expand(self):
        self.setMinimumSize(QSize(900, 750))
        self.resize(900, 750)
        self.dGroupBox.show()
        self.cGroupBox.show()


    def store_s1(self):
        numM = str(self.numMeasure.text())
        numT = str(self.numTreat.text())
        numB = str(self.numBf.text())
        nameM = str(self.nameMeas.text())
        nameD = str(self.namedVar.text())
        self.inputs.s1Inputs = [numM, numT, numB, nameM, nameD]


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
