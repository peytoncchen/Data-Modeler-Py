# Data Modeler for Power Calculations Python Edition

import sys
import pandas as pd
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Mainwindow import Ui_MainWindow
from verify import s1verify, s2verify, s3and4verify, s5verify
from textmanager import preparemultitxt, preparemultisas
from generateglm import makeglmresults, printpwr, exportresultframe, makeftest, fpwr
from inputs import Inputs
from results import Results
from displaypd import pdModel


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
        self.pwrBox.setSpacing(5)
        
        self.fBox = QVBoxLayout()
        self.FScrollWidget.setLayout(self.fBox)
        self.fBox.setSpacing(5)

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
        self.finalexpand = False
        self.firstexpand = False
        self.dViewlabelchanged = False
        self.dViewlabels = []

        self.s1but.clicked.connect(self.s1process)
        self.s2but.clicked.connect(self.s2process)
        self.s4but.clicked.connect(self.s3and4process)
        self.updates4.clicked.connect(self.s3and4update)
        self.s5but.clicked.connect(self.s5process)
        self.addRun.clicked.connect(self.s5add)
        self.editGrid.clicked.connect(self.unlockgrid)
        
        self.exportSAS.clicked.connect(self.exportsas)
        self.glmCalc.clicked.connect(self.runglm)
        self.parsepower.clicked.connect(self.pwr)
        self.exportpwrcsv.clicked.connect(self.exportframes)

        self.actionSave.triggered.connect(self.exporttxt)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionReset.triggered.connect(self.reset)
        self.actionReset.setShortcut("Ctrl+R")
        self.actionDocumentation.triggered.connect(self.opendocs)
        self.actionDocumentation.setShortcut("Ctrl+D")


        completerNmMeaslst = ['Rat', 'Mouse', 'Pig', 'Sheep' 
        'Rabbit', 'Guinea Pig', 'Subject', 'Measurement', 'Sample']
        self.completer1 = QCompleter(completerNmMeaslst, self)
        self.completer1.setCaseSensitivity(0) #Case insensitive
        self.nameMeas.setCompleter(self.completer1)

        completerNmDvarlst = ['Days Survived', 'Time to peak', 'Dependent Variable', 
        'Dependent Var', 'Tumor Size', 'Concentration']
        self.completer2 = QCompleter(completerNmDvarlst, self)
        self.completer2.setCaseSensitivity(0)
        self.namedVar.setCompleter(self.completer2)

        completerNmBF = ['Cage', 'Gender', 'Color', 'Species', 'Age', 'Strain', 'Day', 'Week']
        completerNmBF += completerNmMeaslst[0:11]
        self.completer3 = QCompleter(completerNmBF, self)
        self.completer3.setCaseSensitivity(0)



    def changedViewlabelsbool(self):
        self.dViewlabelchanged = True
    
    def opendocs(self):
        #Links documentation menu button to Github main page with README for user and developer documentation
        webbrowser.open('https://github.com/peytoncchen/Data-Modeler-Py')
        

    def reset(self):
        #Resets everything back to just like first opening the app
        #Storage for app will clear itself when reinitializing that view/calculations so no need to do it here
        self.minimize()
        self.minimize2()
        self.hides6fields()
        self.s2but.hide()
        self.updates4.hide()
        self.updatebool = False
        self.finalexpand = False
        self.firstexpand = False
        self.dViewlabelchanged = False
        self.dViewlabels = []

        self.numMeasure.clear()
        self.numTreat.clear()
        self.numBf.clear()
        self.nameMeas.clear()
        self.namedVar.clear()

        self.numRuns.clear()
        self.experimentName.clear()

        self.clearLayout(self.bFbox)
        self.clearLayout(self.eBox)
        self.clearLayout(self.tBox)

    
    def exportframes(self):
        #Creates file dialog for csv export of resultant dataframes from pairwise t-test after GLM fit
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dataframe = exportresultframe(self.results.resultframes)
        if dlg.exec_():
            dir = dlg.getSaveFileName()
            dataframe.to_csv(str(dir[0]) + '.csv', index=True)


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
        self.pwrBox.addWidget(QLabel(fixedeffect))
        pairwiselabel = QLabel('Power for pairwise t-tests between treatments are estimated as:')
        pairwiselabel.setStyleSheet("font-weight: bold;")
        self.pwrBox.addWidget(pairwiselabel)
        for label in labels:
            self.pwrBox.addWidget(QLabel(label))

    
    def runglm(self):
        #Expands and initializes GLM fit and pairwise t-test multiple comparison for display in QTableViews
        self.statusBar.showMessage('Calculating and fitting GLM models...')
        self.expand2()
        self.clearLayout(self.dfBox)
        self.clearLayout(self.pwrBox) #Since GLM is reinitialized
        self.clearLayout(self.fBox)
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
        for i, tup in enumerate(self.results.fresults):
            string = 'Run ' + str(i+1) + ' | ' + 'f-stat: ' + str(round(tup[0], 4)) + ', ' + 'p-value: ' + str(round(tup[1], 4))
            self.fBox.addWidget(QLabel(string))


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
            view.setMinimumHeight(height)
            self.dfBox.addWidget(view)
        self.statusBar.clearMessage()

    def unlockgrid(self):
        self.results.multiRun.clear()
        self.results.cleardVResultView() #Clears dependent variable generation until update complete
        self.updatedVVal()
        self.s5but.setText('Generate values')
        self.s5but.repaint()
        self.runcounter = 0 #Reset run counter
        self.runCount.setText('Current run count: ' + str(self.runcounter))
        self.runCount.repaint()
        for obj in self.inputs.s5Obj[0]: #Treatment col
            obj.setReadOnly(False)
        for lst in self.inputs.s5Obj[1]: #Blocking fac cols
            for obj in lst:
                obj.setReadOnly(False)


    def lockgrid(self):
        for obj in self.inputs.s5Obj[0]: #Treatment col
            obj.setReadOnly(True)
        for lst in self.inputs.s5Obj[1]: #Blocking fac cols
            for obj in lst:
                obj.setReadOnly(True)

        
    def hides6fields(self):
        #Hides buttons until generated values
        self.addRun.hide()
        self.runCount.hide()
        self.editGrid.hide()
        self.label.hide()
        self.experimentName.hide()
        self.exportSAS.hide()
        self.glmCalc.hide()
        self.numRuns.hide()
    

    def shows6fields(self):
        #Shows buttons after generated values
        self.addRun.show()
        self.addRun.repaint()
        self.runCount.show()
        self.runCount.repaint()
        self.editGrid.show()
        self.editGrid.repaint()
        self.label.show()
        self.label.repaint()
        self.experimentName.show()
        self.experimentName.repaint()
        self.exportSAS.show()
        self.exportSAS.repaint()
        self.glmCalc.show()
        self.glmCalc.repaint()
        self.numRuns.show()
        self.numRuns.repaint()

    
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
            #self.nameMeas.setReadOnly(True) #set read only to prevent weirdness, can edit when the user does total resets
            #self.namedVar.setReadOnly(True)

            self.minimize() #Minimizes 3rd pane if it exists
            #Sets button text to 'Update' after initial press
            self.s1but.setText('Update')
            self.s1but.repaint()
            self.hides6fields() #Need to update everything before being able to S6 stuff
            self.clearLayout(self.cBox) #Clears current input box until everything is updated after S4 (Step 4)
            if self.numMeasure.isModified():
                self.minimize2()
                self.s4but.setText('Continue')
                self.s4but.repaint()
                self.numMeasure.setModified(False)
            if self.numTreat.isModified(): #Only if number of treatments is updated/edited
                self.initTView() 
                self.numTreat.setModified(False)
            if self.numBf.isModified(): #Only if the number of blocking factor is updated/edited
                self.minimize2()
                self.s4but.setText('Continue')
                self.s4but.repaint()
                self.initBfView()
                self.clearLayout(self.eBox) #Clears error box in preparation for update
                if int(self.inputs.s1Inputs[2]) == 0: #handles case where there are 0 blocking factors to initialize error view
                    self.initEView(True) 
                    self.s2but.hide() #in case this is updating from non-zero initial # of blocking factors
                    self.resize(450,751) #trying to get the button to disappear if blocking factors (BF) updated to 0
                    self.resize(450,750) #Weird PyQt5 library-isms??? repaint() and QApplication.processEvents() didn't work
                    self.inputs.s2Inputs.append([]) #To ensure input variables have the same shape even in case of 0 BF
                    self.inputs.s2Inputs.append([])
                else:
                    #Reveals S2 button in case where there are more than 0 blocking factors
                    self.s2but.show()
                    self.s2but.repaint()
            if self.nameMeas.isModified() or self.namedVar.isModified():
                self.nameMeas.setModified(False)
                self.namedVar.setModified(False)
                self.dViewlabelchanged = True
                self.updateDviewlabels() 
                self.dViewlabelchanged = False      
            if self.firstexpand: #If view is not automatically minimized b/c of changes, cleans up view
                self.results.cleardVResultView() #Clears dependent variable generation until update complete
                self.updatedVVal()
                self.s5but.setText('Generate values')
                self.s5but.repaint()
    

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
            self.hides6fields() #Need to update everything and regenerate values before being able to do S6 stuff 
            if self.firstexpand:
                self.results.cleardVResultView() #Clears dependent variable generation until update complete
                self.updatedVVal()
                self.results.genEVals(self.inputs.s2Inputs, self.inputs.s3Inputs)
                self.initcurrInpView() #Reinitializes current input box: if blank, updated needed S3 or S4
                self.s5but.setText('Generate values')
                self.s5but.repaint()
            self.minimize() #Minimizes 3rd pane if it exists


    def s3and4process(self):
        #Continue/reset grid button
        #Store values from step 3 and 4 into an instance of Inputs class created at Mainwindow init
        self.inputs.store_s3and4(self.inputs.s3Obj, self.inputs.s4Obj)

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
            self.s5but.setText('Generate values')
            self.s5but.repaint()
            if not self.firstexpand and not self.finalexpand: #To ensure window resizing isn't awkward
                self.expand()
                self.firstexpand = True
            self.updatebool = False
            self.initDView()
            self.results.genEVals(self.inputs.s2Inputs, self.inputs.s3Inputs)
            self.initcurrInpView()
            self.hides6fields()
            self.minimize() #Minimizes 3rd pane if it exists


    def s3and4update(self):
        #Update errors and treatment means button
        #Store values from step 3 and 4 into an instance of Inputs class created at Mainwindow init
        self.inputs.store_s3and4(self.inputs.s3Obj, self.inputs.s4Obj)

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
            self.results.cleardVResultView()
            self.results.multiRun.clear()
            self.s5but.setText('Generate values')
            self.s5but.repaint()
            self.updatedVVal()
            self.initcurrInpView()
            self.updatebool = True #To update not reinitialize and overwrite current dVVal view
            self.hides6fields() #Rehides buttons until values generated
            self.minimize() #Minimizes 3rd pane if it exists


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
            self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
            self.results.multiRun.clear() #Doubles as reset runs button
            self.results.addRun()
            self.runcounter = 1 #Reset run counter
            self.runCount.setText('Current run count: ' + str(self.runcounter))
            self.minimize()
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
                self.updatedVVal()
                self.numRuns.clear()
                self.statusBar.clearMessage()
            else:
                self.results.gendvVals(self.inputs.s5Inputs, self.inputs.s4Inputs, self.inputs.s3Inputs[0])
                self.runcounter += 1
                self.runCount.setText('Current run count: ' + str(self.runcounter))
                self.runCount.repaint()
                self.updatedVVal()
                self.results.addRun()


    def exporttxt(self):
        #Exports a read-out of current session into text file
        #Includes all inputs, generated error, treatment means, all runs and dVVal generation, power estimation results
        #if they exist. CSV dataframes must be separately exported
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        outstring = preparemultitxt(self.inputs.s5Inputs, self.results.multiRun, self.inputs.s1Inputs, self.inputs.s2Inputs)
        if dlg.exec_():
            dir = dlg.getSaveFileName()
            f = open(str(dir[0]) + '.txt', 'w+')
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
            dir = dlg.getSaveFileName()
            f = open(str(dir[0]) + '.txt', 'w+')
            f.write(outstring)
            f.close()
        self.experimentName.clear()
                  

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


    def updateDviewlabels(self):
        #Updates the distribute view labels if any of the names are changed in step 1 or step 2
        if self.firstexpand and self.dViewlabelchanged:
            self.dViewlabels[0].setText(self.inputs.s1Inputs[3])
            self.dViewlabels[0].repaint()
            for i in range(len(self.inputs.s2Inputs[0])):
                newtext = self.inputs.s2Inputs[0][i]
                self.dViewlabels[i+1].setText(newtext)
                self.dViewlabels[i+1].repaint()
    
    
    def initDView(self):
        #Initializes distribution view in grid format in ScrollArea
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

            iBAssign = []
            for j in range(len(self.inputs.s2Inputs[0])):
                bAssign = QLineEdit()
                bAssign.setFixedHeight(21)
                bAssign.setMaximumWidth(125)
                bAssign.setAlignment(Qt.AlignHCenter)
                iBAssign.append(bAssign)
                self.dGrid.addWidget(bAssign,i+1,j+2)
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
        self.eBox.addRow(totalerror, totalerrorval)
        lsterrors.append(totalerrorval)

        if not emptybool: #if there aren't 0 blocking factors
            for i in range(len(self.inputs.s2Inputs[0])):
                label = QLabel(self.inputs.s2Inputs[0][i] + ' SD:')
                sdval = QLineEdit()
                lsterrors.append(sdval)
                self.eBox.addRow(label, sdval)

        #Stores objects to extract values later
        self.inputs.s3Obj.clear()
        self.inputs.s3Obj = lsterrors


    def initTView(self):
        #Initializes treatment view box based on number of treatments
        self.clearLayout(self.tBox)
        lstmeans = []
        for i in range(int(self.inputs.s1Inputs[1])):
            num = QLabel(str(i + 1))
            mean = QLineEdit()
            lstmeans.append(mean)
            self.tBox.addRow(num, mean)
        
        #Stores objects to extract values later
        self.inputs.s4Obj.clear()
        self.inputs.s4Obj = lstmeans


    def initBfView(self):
        #Initializes blocking factor view box based on number of blocking factors
        self.clearLayout(self.bFbox)
        lstlabel = []
        lstval = []
        for i in range(int(self.inputs.s1Inputs[2])):
            bName = QLineEdit()
            bName.textChanged.connect(self.changedViewlabelsbool)
            bName.setCompleter(self.completer3)
            bVal = QLineEdit()
            lstlabel.append(bName)
            lstval.append(bVal)
            self.bFbox.addRow(bName, bVal)
        
        #Stores objects to extract values later
        self.inputs.s2Obj.clear()
        self.inputs.s2Obj.append(lstlabel)
        self.inputs.s2Obj.append(lstval)


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


    def store_s1(self):
        #Stores the values for S1 into instance of Inputs model created on init
        numM = str(self.numMeasure.text()).strip()
        numT = str(self.numTreat.text()).strip()
        numB = str(self.numBf.text()).strip()
        nameM = str(self.nameMeas.text()).strip()
        nameD = str(self.namedVar.text()).strip()
        self.inputs.s1Inputs = [numM, numT, numB, nameM, nameD]


    def clearLayout(self, layout):
        #Clears the given layout of all widgets
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
