# Data Modeler for Power Calculations Python Edition 
# Dedicated to the Appel Lab at Stanford University Department of Bioengineering
# Developed by Peyton Chen, Summer 2020

# Copyright (C) 2020 Peyton Chen

import sys
import pandas as pd
import numpy as np
import webbrowser
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from modules.Mainwindow import Ui_MainWindow
from modules.verify import s1verify, s2verify, s3and4verify, s5verify, verifygriddict
from modules.textmanager import preparemultitxt, preparemultisas, preparelabeltxt
from modules.generateglm import makeglmresults, printpwr, exportresultframe, makeftest, fpwr
from modules.autofillLD import runLDalgo
from modules.autofillCP import runCPalgo, verifyCPalgo, combotofitgrid
from modules.exportxlsx import writetoxlsx
from modules.inputs import Inputs
from modules.results import Results
from modules.displaypd import pdModel


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self) #From Mainwindow.py

        self.inputs = Inputs() #Initialize classes
        self.results = Results()

        self.runcounter = 0 #Initialize run counter at step 5

        self.bFbox = QFormLayout()
        self.bFscrollWidget.setLayout(self.bFbox) #Blocking factor inputs FormLayout

        self.cBox = QHBoxLayout()
        self.cScrollWidget.setLayout(self.cBox) #Current Inputs View 

        self.tBox = QFormLayout()
        self.tScrollWidget.setLayout(self.tBox) #Treatment inputs FormLayout

        self.eBox = QFormLayout()
        self.eRscrollWidget.setLayout(self.eBox) #Error inputs FormLayout

        self.dGrid = QGridLayout()
        self.dScrollWidget.setLayout(self.dGrid) #Distributing assignments Step 5 GridLayout

        self.dfBox = QVBoxLayout()
        self.GLMScrollWidget.setLayout(self.dfBox) #Dataframes from pairwise t-test GLM VBoxLayout

        self.pwrBox = QVBoxLayout()
        self.PCScrollWidget.setLayout(self.pwrBox) #Power estimate results VBoxLayout
        self.pwrBox.setSpacing(5)
        
        self.fBox = QVBoxLayout()
        self.FScrollWidget.setLayout(self.fBox) #Fixed effect f-test results VBoxLayout
        self.fBox.setSpacing(5)

        self.dGroupBox.hide()
        self.cGroupBox.hide()
        self.GLMGroupBox.hide()
        self.PCGroupBox.hide() #Hiding boxes that won't be shown unless expanded
        self.s2but.setEnabled(False) #Buttons will be enabled when input pane is advanced
        self.s4but.setEnabled(False)
        self.updates4.hide()
        self.editInputs.hide()
        self.hides6fields()

        self.setMinimumSize(QSize(450, 750)) #Setting minimum sizes and resize for pane 1
        self.resize(450, 750)

        self.updatebool = False #Initializing variables
        self.finalexpand = False
        self.firstexpand = False
        self.dViewlabelchanged = False
        self.badexpmt = False
        self.dViewlabels = [] #Will store QLabel objects of labels in the grid so these can be updated w/o reinitialization

        #Connecting events
        self.nameMeas.textChanged.connect(self.changedViewlabelsbool) 
        self.namedVar.textChanged.connect(self.changedViewlabelsbool)

        self.s1but.clicked.connect(self.s1process)
        self.s2but.clicked.connect(self.s2process)
        self.s4but.clicked.connect(self.s3and4process)
        self.updates4.clicked.connect(self.s3and4update)
        self.s5but.clicked.connect(self.s5process)
        self.addRun.clicked.connect(self.s5add)
        self.editGrid.clicked.connect(self.unlockgrid)
        self.loadgridCSV.clicked.connect(self.loadincsv)
        self.editInputs.clicked.connect(self.unlockinputs)
        self.autogenGrid.clicked.connect(self.genGrid)
        
        self.exportTextBut.clicked.connect(self.exporttxt)
        self.exportSAS.clicked.connect(self.exportsas)
        self.glmCalc.clicked.connect(self.runglm)
        self.parsepower.clicked.connect(self.pwr)
        self.exportpwrcsv.clicked.connect(self.exportframes)

        #Status bar events
        self.actionSave.triggered.connect(self.exportxlsx)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionReset.triggered.connect(self.reset)
        self.actionReset.setShortcut("Ctrl+R")
        self.actionDocumentation.triggered.connect(self.opendocs)
        self.actionDocumentation.setShortcut("Ctrl+D")

        self.actionSave_2.triggered.connect(self.savejson)
        self.actionSave_2.setShortcut("Ctrl+J")
        self.actionLoad.triggered.connect(self.loadjson)
        self.actionLoad.setShortcut("Ctrl+L")

        #Timer used in a few places for statusBar background
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.resetSBbkgrd)
        self.timer.start(0) #fixing the fact that SB bkgd color doesn't initialize correctly

        #Setting up QCompleters for labelling/naming
        completerNmMeaslst = ['Rat', 'Mouse', 'Pig', 'Sheep' 
        'Rabbit', 'Guinea Pig', 'Subject', 'Measurement', 'Sample']
        self.completer1 = QCompleter(completerNmMeaslst, self)
        self.completer1.setCaseSensitivity(0) #Case insensitive
        self.nameMeas.setCompleter(self.completer1)

        completerNmDvarlst = ['Days Survived', 'Time to peak', 'Dependent Variable', 
        'Tumor Size', 'Concentration']
        self.completer2 = QCompleter(completerNmDvarlst, self)
        self.completer2.setCaseSensitivity(0)
        self.namedVar.setCompleter(self.completer2)

        completerNmBF = ['Cage', 'Gender', 'Color', 'Species', 'Age', 'Strain', 'Day', 'Week']
        completerNmBF += completerNmMeaslst[0:11]
        self.completer3 = QCompleter(completerNmBF, self)
        self.completer3.setCaseSensitivity(0)
  


    def s1process(self):
        #Continue/Update for initial parameters 
        #Store values from step 1 into an instance of Inputs class created at Mainwindow init
        self.store_s1()

        #Status bar handling in case of unrecognized Step 1 input
        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        verify = s1verify(self.inputs.s1Inputs) #Returns bool and string description of error
        if not verify[0]:
            self.statusBar.showMessage(verify[1])
            self.statusBar.setStyleSheet("background-color: pink;")
            return #if unrecognized inputs program will not continue and halt here
        else:
            self.minimize() #Minimizes 3rd pane if it exists
            #Sets button text to 'Update' after initial press
            self.s1but.setText('Update')
            self.s1but.repaint()
            self.s4but.setEnabled(True)
            if self.numMeasure.isModified():
                self.minimize2()
                self.s4but.setText('Continue')
                self.s4but.repaint()
                self.updates4.hide()
                self.updates4.repaint()
                self.numMeasure.setModified(False)
            if self.numTreat.isModified(): #Only if number of treatments is updated/edited
                self.initTView() 
                self.numTreat.setModified(False)
                self.clearLayout(self.cBox) #Clears current input box until everything is updated after S4 (Step 4)
            if self.numBf.isModified(): #Only if the number of blocking factor is updated/edited
                self.minimize2()
                self.s4but.setText('Continue')
                self.s4but.repaint()
                self.updates4.hide()
                self.updates4.repaint()
                self.initBfView()
                self.clearLayout(self.eBox) #Clears error box in preparation for update
                if int(self.inputs.s1Inputs[2]) == 0: #handles case where there are 0 blocking factors to initialize error view
                    self.initEView(True) 
                    self.s2but.setEnabled(False) #in case this is updating from non-zero initial # of blocking factors
                    self.s2but.setText('Skip this!')
                    self.s2but.repaint()
                    self.inputs.s2Inputs.append([]) #To ensure input variables have the same shape even in case of 0 BF
                    self.inputs.s2Inputs.append([])
                else:
                    #Reveals S2 button in case where there are more than 0 blocking factors
                    self.s2but.setEnabled(True)
                    self.s2but.repaint()
            if self.dViewlabelchanged:
                self.updateDviewlabels()
                self.dViewlabelchanged = False  
            if self.firstexpand:
                self.unlockgrid()
    

    def s2process(self):
        #Continue/Update for assigning blocking factor names and number
        #Store values from step 2 into an instance of Inputs class created at Mainwindow init
        self.inputs.store_s2(self.inputs.s2Obj[0], self.inputs.s2Obj[1])

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        verify = s2verify(self.inputs.s2Inputs)
        if not verify[0]:
            self.statusBar.showMessage(verify[1])
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            if self.numBf.isModified(): #Only reinitializes Error Step 3 View if Step 1 number of blocking factors is changed/updated
                self.initEView(False)
                self.numBf.setModified(False)
            if self.dViewlabelchanged:
                self.updateDviewlabels()
                self.dViewlabelchanged = False
            self.s2but.setText('Update')
            self.s2but.repaint()
            if self.firstexpand:
                self.unlockgrid()
                self.results.genEVals(self.inputs.s2Inputs, self.inputs.s3Inputs)
                self.initcurrInpView() #Reinitializes current input box: if blank, updated needed S3 or S4



    def s3and4process(self):
        #Continue/reset grid button
        #Store values from step 3 and 4 into an instance of Inputs class created at Mainwindow init
        self.inputs.store_s3and4(self.inputs.s3Obj, self.inputs.s4Obj, self.inputs.s4labelobj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        verify = s3and4verify(self.inputs.s3Inputs, self.inputs.s4Inputs)
        if not verify[0]:
            self.statusBar.showMessage(verify[1])
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.s4but.setText('Reinitialize grid')
            self.s4but.repaint()
            if not self.firstexpand and not self.finalexpand: #To ensure window resizing isn't awkward
                self.expand()
                self.firstexpand = True
            self.updatebool = False
            self.initDView()
            self.results.genEVals(self.inputs.s2Inputs, self.inputs.s3Inputs)
            self.initcurrInpView()
            self.unlockgrid()


    def s3and4update(self):
        #Update errors and treatment means button
        #Store values from step 3 and 4 into an instance of Inputs class created at Mainwindow init
        self.inputs.store_s3and4(self.inputs.s3Obj, self.inputs.s4Obj, self.inputs.s4labelobj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        verify = s3and4verify(self.inputs.s3Inputs, self.inputs.s4Inputs)
        if not verify[0]:
            self.statusBar.showMessage(verify[1])
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            #Generates new error values and clears any current/outdated dependent variables
            self.results.genEVals(self.inputs.s2Inputs, self.inputs.s3Inputs)
            self.initcurrInpView()
            self.updatebool = True #To update not reinitialize and overwrite current dVVal view
            self.unlockgrid()


    def s5process(self):
        #Generate values/reset runs button
        #Store values from step 5 (distribution grid) into an instance of Inputs class created at Mainwindow init
        self.inputs.stores_s5(self.inputs.s5Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        verify = s5verify(self.inputs.s5Inputs, self.inputs.s1Inputs, self.inputs.s2Inputs)
        if not verify[0]:
            self.statusBar.showMessage(verify[1])
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.lockgrid()
            self.lockinputs()
            self.editInputs.show()
            self.editInputs.repaint()
            self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
            self.results.multiRun.clear() #Doubles as reset runs button
            self.results.addRun()
            self.runcounter = 1 #Reset run counter
            self.runCount.setText('Current run count: ' + str(self.runcounter))
            self.runCount.repaint()
            self.minimize()
            if not self.updatebool:
                self.initdVValView()
                self.s5but.setText('Reset runs')
                self.s5but.repaint()
                self.updates4.show()
                self.updates4.repaint()
                self.shows6fields()
            else:
                self.shows6fields()
                self.updatedVVal()
                self.runCount.repaint()
                self.updatebool = True    


    def s5add(self):
        #Add runs button
        self.inputs.stores_s5(self.inputs.s5Obj)

        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: none;")

        verify = s5verify(self.inputs.s5Inputs, self.inputs.s1Inputs, self.inputs.s2Inputs)
        if not verify[0]:
            self.statusBar.showMessage(verify[1])
            self.statusBar.setStyleSheet("background-color: pink;")
            return
        else:
            self.statusBar.clearMessage()
            self.statusBar.setStyleSheet("background-color: none;")
            self.minimize()
            if self.runcounter > 2000:
                self.statusBar.showMessage('Are you trying to crash the program??? Error - Too many runs')
                self.statusBar.setStyleSheet("background-color: pink;")
                return
            if str(self.numRuns.text()):
                try:
                    numR = int(str(self.numRuns.text()))
                except ValueError:
                    self.statusBar.showMessage('Invalid input - Number of runs must be integer')
                    self.statusBar.setStyleSheet("background-color: pink;")
                    return
                if numR < 0:
                    self.statusBar.showMessage('Invalid input - Number of runs must be positive')
                    self.statusBar.setStyleSheet("background-color: pink;")
                    return
                self.statusBar.showMessage('Calculating...')
                for i in range(numR):
                    self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
                    self.runcounter += 1
                    self.results.addRun()
                self.runCount.setText('Current run count: ' + str(self.runcounter))
                self.runCount.repaint()
                self.runCount.adjustSize()
                self.updatedVVal()
                self.numRuns.clear()
                self.numRuns.repaint()
                self.statusBar.clearMessage()
            else:
                self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
                self.runcounter += 1
                self.runCount.setText('Current run count: ' + str(self.runcounter))
                self.runCount.repaint()
                self.updatedVVal()
                self.results.addRun()


    def loadincsv(self):
        self.unlockgrid()
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        filename, _filter = dlg.getOpenFileName(None, "Load in csv", ".", "(*.csv)")

        if filename:
            grid = pd.read_csv(str(filename))
            griddict = grid.to_dict('list') #list format extraction of dataframe to dict

            verify = verifygriddict(griddict, self.inputs.s1Inputs, self.inputs.s2Inputs)
            self.statusBar.clearMessage()
            self.statusBar.setStyleSheet("background-color: none;")

            if not verify[0]:
                self.statusBar.showMessage(verify[1])
                self.statusBar.setStyleSheet("background-color: pink;")
                return
            else:
                self.inputs.loadin_s5(self.inputs.s5Obj, griddict)
    

    def genGrid(self):
        choices = ('Cartesian product assignment (Default)', 'Quasi-random low discrepancy sequence assignment')
        choice, ok = QInputDialog.getItem(self, 'Select auto-gen method', 'Note: Use cartesian product for all but very large sample sizes.', choices, 0 , False)
        if ok and choice:
            self.unlockgrid()

            if choice == 'Cartesian product assignment (Default)':
                combos = runCPalgo(self.inputs.s1Inputs, self.inputs.s2Inputs)
                verify = verifyCPalgo(self.inputs.s1Inputs, combos)
                self.statusBar.clearMessage()
                self.statusBar.setStyleSheet("background-color: none;")

                if not verify[0]:
                    self.statusBar.showMessage(verify[1])
                    self.statusBar.setStyleSheet("background-color: pink;") #Light yellow warning
                    return #will not fit to grid unless #of measurements is multiple of combos
                else:
                    dic = combotofitgrid(combos, self.inputs.s2Inputs, self.inputs.s1Inputs)
                    self.inputs.loadin_s5(self.inputs.s5Obj, dic)

            if choice == 'Quasi-random low discrepancy sequence assignment':
                dic = runLDalgo(self.inputs.s1Inputs, self.inputs.s2Inputs)

                verify = verifygriddict(dic, self.inputs.s1Inputs, self.inputs.s2Inputs)
                self.statusBar.clearMessage()
                self.statusBar.setStyleSheet("background-color: none;")

                if not verify[0]:
                    self.statusBar.showMessage('Auto-generation is an experimental feature... it did something wrong, going to have to grid in yourself or try Cartesian product!') 
                    self.statusBar.setStyleSheet("background-color: pink;")
                    return
                else:
                    self.statusBar.setStyleSheet("background-color: #FFFF99") #Light yellow warning
                    self.timer.start(5000)
                    self.statusBar.showMessage('Experimental feature - there may be a better distribution if done by hand or cartesian product', 5000)
                    self.inputs.loadin_s5(self.inputs.s5Obj, dic)


    def runglm(self):
        #Expands and initializes GLM fit and pairwise t-test multiple comparison for display in QTableViews
        self.expand2()
        self.clearLayout(self.dfBox)
        self.clearLayout(self.pwrBox) #Since GLM is reinitialized
        self.clearLayout(self.fBox)
        self.badexpmt = False

        results = makeglmresults(self.inputs.s5Inputs, self.results.multiRun, self.inputs.s1Inputs, self.inputs.s2Inputs)
        resultframes = results[0]
        bigmodels = results[1]
        self.results.resultframes.clear()
        self.results.resultframes = resultframes

        fresults = makeftest(self.inputs.s5Inputs, self.results.multiRun, self.inputs.s1Inputs, self.inputs.s2Inputs, bigmodels)
        self.results.fresults.clear()
        self.results.fresults = fresults
        #Initializing text for display in f-test box
        self.fBox.addWidget(QLabel('Fixed effects f-test results:'))
        fstring = ''

        for i, tup in enumerate(self.results.fresults):
            fstring += 'Run ' + str(i+1) + ' | ' + 'f-stat: ' + str(round(tup[0], 4)) + ', ' + 'p-value: ' + str(round(tup[1], 4))
            fstring += '\n'
            if tup[0] == -np.inf or tup[0] == np.inf:
                self.badexpmt = True
        
        flabel = QLabel(fstring)
        self.results.fstring = fstring
        flabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        flabel.setCursor(Qt.IBeamCursor)
        self.fBox.addWidget(flabel)

        if self.badexpmt:
            self.statusBar.setStyleSheet("background-color: #FFFF99") #Light yellow warning
            self.statusBar.showMessage('Warning - this experiment is designed without enough separation in treatment and blocking factor assignments, unable to complete f-test', 10000)
            self.timer.start(10000)

        #Initializing tableviews for pairwise t-test
        self.dfBox.addWidget(QLabel('Pairwise t-test results:'))
        for frame in self.results.resultframes:
            model = pdModel(frame)
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
            view.setFixedHeight(height) #locks in height
            self.dfBox.addWidget(view)
        self.dfBox.addStretch() #Fill in empty space if there aren't enough tables generated

    
    def pwr(self):
        #Initializes display after parsing power with power estimation results
        self.clearLayout(self.pwrBox)
        labels = printpwr(self.results.resultframes)
        headpwrlabel = QLabel('Based on ' + str(len(self.results.multiRun)) + ' runs and alpha = 0.05:')
        headpwrlabel.setStyleSheet("font-weight: bold;")
        self.pwrBox.addWidget(headpwrlabel)
        

        fixedlabel = QLabel('Power for fixed effect f-test is estimated as:')
        fixedlabel.setStyleSheet("font-weight: bold;")
        self.pwrBox.addWidget(fixedlabel)
        fixedeffect = fpwr(self.results.fresults)
        self.results.fpwrstring = fixedeffect
        fixedeffectresult = QLabel(fixedeffect)
        fixedeffectresult.setTextInteractionFlags(Qt.TextSelectableByMouse)
        fixedeffectresult.setCursor(Qt.IBeamCursor)
        self.pwrBox.addWidget(fixedeffectresult)

        pairwiselabel = QLabel('Power for pairwise t-tests between treatments are estimated as:')
        pairwiselabel.setStyleSheet("font-weight: bold;")
        self.pwrBox.addWidget(pairwiselabel)
        pairwiseresultstr = ''
        for label in labels:
            pairwiseresultstr += label
            pairwiseresultstr += '\n'
        pairwiseresult = QLabel(pairwiseresultstr)
        self.results.pstring = pairwiseresultstr
        pairwiseresult.setTextInteractionFlags(Qt.TextSelectableByMouse)
        pairwiseresult.setCursor(Qt.IBeamCursor)
        self.pwrBox.addWidget(pairwiseresult)


    def exportframes(self):
        #Creates file dialog for csv export of resultant dataframes from pairwise t-test after GLM fit
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dataframe = exportresultframe(self.results.resultframes)
        if dlg.exec_():
            directory, _filter = dlg.getSaveFileName()
            dataframe.to_csv(str(directory) + '.csv', index=True)


    def exporttxt(self):
        #Exports a read-out of all runs and only runs into text file
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        outstring = preparemultitxt(self.inputs.s5Inputs, self.results.multiRun, self.inputs.s1Inputs, self.inputs.s2Inputs)
        if dlg.exec_():
            directory, _filter = dlg.getSaveFileName()
            f = open(str(directory) + '.txt', 'w+')
            f.write(outstring)
            f.close()


    def exportsas(self):
        #Exports SAS script in a text file for multiple comparison tests with Tukey correction. This can be done in house!
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if self.experimentName.text() == '': #Sets experiment name as 'UnnamedExpmt' if nothing is inputted befores gen script
            self.experimentName.setText('UnnamedExpmt')
            self.experimentName.repaint()
        outstring = preparemultisas(self.inputs.s5Inputs, self.results.multiRun, self.inputs.s1Inputs, 
        self.inputs.s2Inputs, self.experimentName.text())
        if dlg.exec_():
            directory, _filter = dlg.getSaveFileName()
            f = open(str(directory) + '.txt', 'w+')
            f.write(outstring)
            f.close()
        self.experimentName.clear() #Clears experiment name

    
    def exportxlsx(self):
        #Exports a read-out of current session into excel file
        #Includes all inputs, generated error, treatment means, all runs and dVVal generation, power estimation results
        #if they exist. CSV dataframes must be separately exported
        if self.updatebool:
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.Directory)
            if dlg.exec_():
                directory, _filter = dlg.getSaveFileName()
                labels = preparelabeltxt(self.inputs.s1Inputs, self.inputs.s2Inputs)
                writetoxlsx(self.inputs.s1Inputs, self.inputs.s2Inputs, self.inputs.s3Inputs, self.inputs.s4Inputs, 
                self.inputs.s4labels, self.inputs.s5Inputs, self.results.multiRun, self.results.fstring, self.results.fpwrstring,
                self.results.pstring, labels, self.results.errorResults, directory)
                
        else:
            self.statusBar.setStyleSheet("background-color: #FFFF99")
            self.statusBar.showMessage('Generate some values before you export to xlsx!', 7000)
            self.timer.start(7000)

    
    def savejson(self):
        #Saves to json so that user can load in data from a session later
        if self.results.multiRun: #Can't be empty to save
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.Directory)
            if dlg.exec_():
                directory, _filter = dlg.getSaveFileName()
                outdic = {}
                outdic['s1Inputs'] = self.inputs.s1Inputs
                outdic['s2Inputs'] = self.inputs.s2Inputs
                outdic['s3Inputs'] = self.inputs.s3Inputs
                outdic['s4Inputs'] = self.inputs.s4Inputs
                outdic['s4labels'] = self.inputs.s4labels
                outdic['s5Inputs'] = self.inputs.s5Inputs
                outdic['errorResults'] = self.results.errorResults
                outdic['multiRun'] = self.results.multiRun
                outdic['finalexpand'] = self.finalexpand
                with open(str(directory) + '.json', 'w') as write_file:
                    json.dump(outdic,write_file)
        else:
            self.statusBar.setStyleSheet("background-color: #FFFF99")
            self.statusBar.showMessage('Generate some values before you export to json!', 7000)
            self.timer.start(7000)


    def loadjson(self):
        self.reset() #Resets to prepare for loading in
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        filename, _filter = dlg.getOpenFileName(None, "Load in json", ".", "(*.json)")

        if filename:
            self.reset()
            with open(filename, 'r') as read_file:
                indic = json.load(read_file)

                #Set text for S1
                self.numMeasure.setText(indic['s1Inputs'][0])
                self.numMeasure.setModified(True)
                self.numMeasure.repaint()
                self.numTreat.setText(indic['s1Inputs'][1])
                self.numTreat.setModified(True)
                self.numTreat.repaint()
                self.numBf.setText(indic['s1Inputs'][2])
                self.numBf.setModified(True)
                self.numBf.repaint()
                self.nameMeas.setText(indic['s1Inputs'][3])
                self.nameMeas.setModified(True)
                self.nameMeas.repaint()
                self.namedVar.setText(indic['s1Inputs'][4])
                self.namedVar.setModified(True)
                self.namedVar.repaint()
                self.s1process()

                #Set text for S2
                for i, obj in enumerate(self.inputs.s2Obj[0]): #labels
                    obj.setText(indic['s2Inputs'][0][i])
                    obj.repaint()
                for i, obj in enumerate(self.inputs.s2Obj[1]): #values
                    obj.setText(indic['s2Inputs'][1][i])
                    obj.repaint()
                self.s2process()

                #Set text for S3
                for i, obj in enumerate(self.inputs.s3Obj):
                    obj.setText(indic['s3Inputs'][i])
                    obj.repaint()

                #Set text for S4
                for i, obj in enumerate(self.inputs.s4Obj):
                    obj.setText(indic['s4Inputs'][i])
                    obj.repaint()
                for i, obj in enumerate(self.inputs.s4labelobj):
                    obj.setText(indic['s4labels'][i])
                    obj.repaint()
                self.s3and4process()

                #Set text for S5 and storage
                self.results.multiRun = indic['multiRun']
                self.results.dVResults = self.results.multiRun[-1] 
                self.initdVValView()
                self.results.errorResults = indic['errorResults']
                self.initcurrInpView()
                self.inputs.s5Inputs = indic['s5Inputs']
                for i, obj in enumerate(self.inputs.s5Obj[0]): #Treatment col
                    obj.setText(indic['s5Inputs'][0][i])
                    obj.repaint()
                for i,lst in enumerate(self.inputs.s5Obj[1]): #Blocking fac cols
                    for j,obj in enumerate(lst):
                        obj.setText(indic['s5Inputs'][1][i][j])
                        obj.repaint()
                self.lockgrid()
                self.lockinputs()
                self.editInputs.show()
                self.editInputs.repaint()
                self.runcounter = len(self.results.multiRun)
                self.runCount.setText('Current run count: ' + str(self.runcounter))
                self.runCount.repaint()
                self.s5but.setText('Reset runs')
                self.s5but.repaint()
                self.updates4.show()
                self.updates4.repaint()
                self.shows6fields()

                if indic['finalexpand']:
                    self.runglm()
                    self.pwr()                      
                  

    def initcurrInpView(self):
        #Current inputs box display initialization
        self.clearLayout(self.cBox)
        self.errors = QLabel()
        self.tmeans = QLabel()
        #To make the text copyable
        self.errors.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.errors.setCursor(Qt.IBeamCursor)
        self.tmeans.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.tmeans.setCursor(Qt.IBeamCursor)
        self.errors.setAlignment(Qt.AlignTop)
        self.tmeans.setAlignment(Qt.AlignTop)
        self.cBox.addWidget(self.errors) #in a hbox
        self.cBox.addWidget(self.tmeans)

        generrors = ''
        tmeans = 'Treatment Means:\n'

        #For generated error
        for i in range(len(self.inputs.s2Inputs[0])):
            generrors += self.inputs.s2Inputs[0][i] + ' SD generated error:\n'
            for j in range(len(self.results.errorResults[i])):
                generrors += str(j + 1)
                generrors += ': '
                generrors += str(self.results.errorResults[i][j])
                generrors += '\n'
            generrors += '\n'

        #For treatment means
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
        #Updates dependent var generation text with setText rather than overwriting
        for i in range(len(self.results.dVResults)):
            self.results.dVObjects[i].setText(str(self.results.dVResults[i]))
            self.results.dVObjects[i].repaint()
            

    def initdVValView(self):
        #Initializes dvVal View in newly generated grid when the view doesn't exist yet
        labellst = []
        colCount = int(self.inputs.s1Inputs[2]) + 2
        
        for i in range(len(self.results.dVResults)):
            label = QLabel(str(self.results.dVResults[i]))
            label.setAlignment(Qt.AlignHCenter)
            label.setFixedHeight(21)
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            label.setCursor(Qt.IBeamCursor)
            labellst.append(label)
            self.dGrid.addWidget(label,i+1,colCount)
        self.results.dVObjects = labellst
        self.updatebool = True


    def updateDviewlabels(self):
        #Updates the distribute view labels if any of the names are changed in step 1 or step 2
        if self.firstexpand and self.dViewlabels:
            self.dViewlabels[0].setText(self.inputs.s1Inputs[3])
            self.dViewlabels[0].repaint()
            for i in range(len(self.inputs.s2Inputs[0])):
                newtext = self.inputs.s2Inputs[0][i]
                self.dViewlabels[i+1].setText(newtext)
                self.dViewlabels[i+1].repaint()
            self.dViewlabels[len(self.dViewlabels) - 1].setText(self.inputs.s1Inputs[4])
            self.dViewlabels[len(self.dViewlabels) - 1].repaint()
    
    
    def initDView(self):
        #Initializes distribution view in grid format in ScrollArea
        self.clearLayout(self.dGrid)
        tAssignObj = []
        bAssignObj = []
        self.dViewlabels.clear()

        #Init the row labels
        l1 = QLabel(self.inputs.s1Inputs[3])
        l2 = QLabel("Treatment")
        l1.setAlignment(Qt.AlignHCenter)
        l2.setAlignment(Qt.AlignHCenter)
        l1.setFixedHeight(21)
        l2.setFixedHeight(21)
        self.dGrid.addWidget(l1,0,0)
        self.dGrid.addWidget(l2,0,1)
        self.dViewlabels.append(l1)
        #self.dViewlabels.append(l2) Skipped because this will always be treatment

        for i in range(len(self.inputs.s2Inputs[0])):
            blabel = QLabel(self.inputs.s2Inputs[0][i])
            blabel.setFixedHeight(21)
            blabel.setAlignment(Qt.AlignHCenter)
            self.dGrid.addWidget(blabel,0,i+2)
            self.dViewlabels.append(blabel)

        colCount = int(self.inputs.s1Inputs[2]) + 2
        name = QLabel(self.inputs.s1Inputs[4])
        name.setAlignment(Qt.AlignHCenter)
        name.setFixedHeight(21)
        self.dGrid.addWidget(name,0,colCount)
        self.dViewlabels.append(name)

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
            tAssign.repaint()

            iBAssign = []
            for j in range(len(self.inputs.s2Inputs[0])):
                bAssign = QLineEdit()
                bAssign.setFixedHeight(21)
                bAssign.setMaximumWidth(125)
                bAssign.setAlignment(Qt.AlignHCenter)
                iBAssign.append(bAssign)
                self.dGrid.addWidget(bAssign,i+1,j+2)
                bAssign.repaint()
            bAssignObj.append(iBAssign)

        #Store these inputs to extract values at a later time
        self.inputs.s5Obj.clear()
        self.inputs.s5Obj.append(tAssignObj)
        self.inputs.s5Obj.append(bAssignObj)

    
    def initEView(self,emptybool):
        #Initializes inputting error SD's for total and all the blocking factors
        self.clearLayout(self.eBox)
        lsterrors = []

        totalerror = QLabel("Total error SD:")
        totalerrorval = QLineEdit()
        totalerrorval.setPlaceholderText('Enter SD value')
        self.eBox.addRow(totalerror, totalerrorval)
        lsterrors.append(totalerrorval)

        if not emptybool: #if there aren't 0 blocking factors
            for i in range(len(self.inputs.s2Inputs[0])):
                label = QLabel(self.inputs.s2Inputs[0][i] + ' SD:')
                sdval = QLineEdit()
                sdval.setPlaceholderText('Enter SD value')
                lsterrors.append(sdval)
                self.eBox.addRow(label, sdval)
                label.repaint()
                sdval.repaint()

        #Stores objects to extract values later
        self.inputs.s3Obj.clear()
        self.inputs.s3Obj = lsterrors


    def initTView(self):
        #Initializes treatment view box based on number of treatments
        self.clearLayout(self.tBox)
        lstmeans = []
        lsttlabels = []
        for i in range(int(self.inputs.s1Inputs[1])):
            num = QLabel(str(i + 1))

            label = QLineEdit()
            label.setPlaceholderText('Enter label (opt)')
            lsttlabels.append(label)
            mean = QLineEdit()
            mean.setPlaceholderText('Enter mean')

            hbox = QHBoxLayout()
            hbox.addWidget(label)
            hbox.addWidget(mean)

            lstmeans.append(mean)
            self.tBox.addRow(num, hbox)
            num.repaint()
            mean.repaint()
        
        #Stores objects to extract values later
        self.inputs.s4Obj.clear()
        self.inputs.s4Obj = lstmeans
        self.inputs.s4labelobj.clear()
        self.inputs.s4labelobj = lsttlabels


    def initBfView(self):
        #Initializes blocking factor view box based on number of blocking factors
        self.clearLayout(self.bFbox)
        lstlabel = []
        lstval = []
        for i in range(int(self.inputs.s1Inputs[2])):
            bName = QLineEdit()
            bName.textChanged.connect(self.changedViewlabelsbool)
            bName.setCompleter(self.completer3)
            bName.setPlaceholderText('Enter label')
            bVal = QLineEdit()
            bVal.setPlaceholderText('Enter value')
            lstlabel.append(bName)
            lstval.append(bVal)
            self.bFbox.addRow(bName, bVal)
            bName.repaint()
            bVal.repaint()
        
        #Stores objects to extract values later
        self.inputs.s2Obj.clear()
        self.inputs.s2Obj.append(lstlabel)
        self.inputs.s2Obj.append(lstval)


    def lockinputs(self):
        #Locks input QLineEdits and QPushButtons for pane 1
        self.editInputs.setEnabled(True)
        self.editInputs.repaint()

        #Locking out S1
        self.numMeasure.setReadOnly(True)
        self.numTreat.setReadOnly(True)
        self.numBf.setReadOnly(True)
        self.nameMeas.setReadOnly(True)
        self.namedVar.setReadOnly(True)
        self.s1but.setEnabled(False)
        self.s1but.repaint()
        
        #Locking out S2
        for obj in self.inputs.s2Obj[0]:
            obj.setReadOnly(True)
        for obj in self.inputs.s2Obj[1]:
            obj.setReadOnly(True)
        self.s2but.setEnabled(False)
        self.s2but.repaint()

        #Locking out S3
        for obj in self.inputs.s3Obj:
            obj.setReadOnly(True)
        
        #Locking out S4
        for obj in self.inputs.s4Obj:
            obj.setReadOnly(True)
        for obj in self.inputs.s4labelobj:
            obj.setReadOnly(True)
        self.s4but.setEnabled(False)
        self.s4but.repaint()
        self.updates4.setEnabled(False)
        self.updates4.repaint()


    def unlockinputs(self):
        #Unlocks QLineEdits and QPushButtons to update inputs for pane 1
        self.editInputs.setEnabled(False)
        self.editInputs.repaint()
        self.minimize()

        if self.firstexpand:
            self.unlockgrid()

        #Unlocking S1
        self.numMeasure.setReadOnly(False)
        self.numTreat.setReadOnly(False)
        self.numBf.setReadOnly(False)
        self.nameMeas.setReadOnly(False)
        self.namedVar.setReadOnly(False)
        self.s1but.setEnabled(True)
        self.s1but.repaint()

        #Unlocking S2
        if self.inputs.s2Obj:
            for obj in self.inputs.s2Obj[0]:
                obj.setReadOnly(False)
            for obj in self.inputs.s2Obj[1]:
                obj.setReadOnly(False)
            if int(self.inputs.s1Inputs[2]) != 0:
                self.s2but.setEnabled(True)
                self.s2but.repaint()

        #Unlocking S3
        if self.inputs.s3Obj:
            for obj in self.inputs.s3Obj:
                obj.setReadOnly(False)
        
        #Unlocking S4
        if self.inputs.s4Obj:
            for obj in self.inputs.s4Obj:
                obj.setReadOnly(False)
            for obj in self.inputs.s4labelobj:
                obj.setReadOnly(False)
            self.s4but.setEnabled(True)
            self.s4but.repaint()
            self.updates4.setEnabled(True)
            self.updates4.repaint()


    def unlockgrid(self):
        #Unlocks distribution grid on pane 2
        self.hides6fields()
        self.results.multiRun.clear()
        self.runcounter = 0
        self.runCount.setText('Current run count: ' + str(self.runcounter))
        self.runCount.repaint()
        if self.updatebool: #So this doesn't crash out on reset since QLabel objects are deleted
            self.results.cleardVResultView() #Clears dependent variable generation until update complete
            self.updatedVVal()
        self.s5but.setText('Generate values')
        self.s5but.repaint()
        self.minimize()
        if self.inputs.s5Obj: #if not empty
            for obj in self.inputs.s5Obj[0]: #Treatment col
                obj.setReadOnly(False)
            for lst in self.inputs.s5Obj[1]: #Blocking fac cols
                for obj in lst:
                    obj.setReadOnly(False)


    def lockgrid(self):
        #Locks distribution grid on pane 2
        for obj in self.inputs.s5Obj[0]: #Treatment col
            obj.setReadOnly(True)
        for lst in self.inputs.s5Obj[1]: #Blocking fac cols
            for obj in lst:
                obj.setReadOnly(True)

    
    def changedViewlabelsbool(self):
        #Changes bool dViewlabelchanged to True
        self.dViewlabelchanged = True

    
    def resetSBbkgrd(self):
        #Changes status bar background back to none
        self.statusBar.setStyleSheet("background-color: none;")
  
    
    def opendocs(self):
        #Links documentation menu button to Github main page with README for user and developer documentation
        webbrowser.open('https://github.com/peytoncchen/Data-Modeler-Py')
        

    def reset(self):
        #Resets everything back to just like first opening the app
        #Storage for app will clear itself when reinitializing that view/calculations so no need to do it here
        self.unlockinputs()
        self.minimize()
        self.minimize2()
        self.hides6fields()
        self.s2but.setEnabled(False)
        self.s4but.setEnabled(False)
        self.updates4.hide()
        self.editInputs.hide()
        self.updatebool = False
        self.finalexpand = False
        self.firstexpand = False
        self.dViewlabelchanged = False
        self.badexpmt = False
        self.dViewlabels = []

        self.numMeasure.clear()
        self.numTreat.clear()
        self.numBf.clear()
        self.nameMeas.clear()
        self.namedVar.clear()

        self.inputs.s2Obj.clear()
        self.inputs.s3Obj.clear()
        self.inputs.s4Obj.clear()
        self.inputs.s4labelobj.clear()
        self.inputs.s5Obj.clear()
        self.results.dVObjects.clear()

        self.numRuns.clear()
        self.experimentName.clear()

        self.clearLayout(self.bFbox)
        self.clearLayout(self.eBox)
        self.clearLayout(self.tBox)

        self.s1but.setText('Continue')
        self.s1but.repaint()
        self.s2but.setText('Continue')
        self.repaint()
        self.s4but.setText('Continue')
        self.s4but.repaint()
        self.s5but.setText('Generate values')
        self.s5but.repaint()


    def hides6fields(self):
        #Disables buttons and set readonly QLineEdit until generated values for step 6
        self.addRun.setEnabled(False)
        self.numRuns.setReadOnly(True)
        self.editGrid.setEnabled(False)
        self.exportSAS.setEnabled(False)
        self.glmCalc.setEnabled(False)
        self.experimentName.setReadOnly(True)
        self.exportTextBut.setEnabled(False)
        self.exportTextBut.repaint()
        self.addRun.repaint()
        self.editGrid.repaint()
        self.experimentName.repaint()
        self.exportSAS.repaint()
        self.glmCalc.repaint()
        self.numRuns.repaint()
    

    def shows6fields(self):
        #Enables buttons and allow edit QLineEdit after generated values for step 6
        self.addRun.setEnabled(True)
        self.numRuns.setReadOnly(False)
        self.editGrid.setEnabled(True)
        self.exportSAS.setEnabled(True)
        self.glmCalc.setEnabled(True)
        self.experimentName.setReadOnly(False)
        self.exportTextBut.setEnabled(True)
        self.exportTextBut.repaint()
        self.addRun.repaint()
        self.editGrid.repaint()
        self.experimentName.repaint()
        self.exportSAS.repaint()
        self.glmCalc.repaint()
        self.numRuns.repaint()


    def expand2(self):
        #Final expand for GLM pane
        self.finalexpand = True
        self.resize(1350, 750)
        self.setMinimumSize(QSize(1350, 750))
        self.GLMGroupBox.show()
        self.PCGroupBox.show()


    def expand(self):
        #First expand for dvVal generation
        self.firstexpand = True
        self.resize(900, 750)
        self.setMinimumSize(QSize(900, 750))
        self.dGroupBox.show()
        self.cGroupBox.show()


    def minimize(self):
        #Minimizes the 3rd GLM pane
        if self.finalexpand:
            self.finalexpand = False
            self.GLMGroupBox.hide()
            self.PCGroupBox.hide()
            self.setMinimumSize(QSize(900, 750))
            self.resize(900, 750)


    def minimize2(self):
        #Minimizes the 2nd pane
        if self.firstexpand:
            self.firstexpand = False
            self.updates4.hide()
            self.dGroupBox.hide()
            self.cGroupBox.hide()
            self.setMinimumSize(QSize(450, 750))
            self.resize(450, 750)


    def store_s1(self):
        #Stores the values for S1 into instance of Inputs model created on init
        #Function is here and not inputs class since this is part of static UI
        numM = str(self.numMeasure.text()).strip()
        numT = str(self.numTreat.text()).strip()
        numB = str(self.numBf.text()).strip()
        nameM = str(self.nameMeas.text()).strip()
        nameD = str(self.namedVar.text()).strip()
        self.inputs.s1Inputs = [numM, numT, numB, nameM, nameD]


    def clearLayout(self, layout):
        #Clears the given layout of all widgets      
        if layout is not None:
            while layout.count():
                c = layout.takeAt(0)
                widget = c.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(c.layout())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
