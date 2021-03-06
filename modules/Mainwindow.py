# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1350, 780)
        MainWindow.setMinimumSize(QtCore.QSize(1350, 750))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.inputGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.inputGroupBox.setMinimumSize(QtCore.QSize(360, 220))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.inputGroupBox.setFont(font)
        self.inputGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.inputGroupBox.setFlat(False)
        self.inputGroupBox.setCheckable(False)
        self.inputGroupBox.setObjectName("inputGroupBox")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.inputGroupBox)
        self.verticalLayout_1.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_1.setSpacing(2)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.formLayout1 = QtWidgets.QFormLayout()
        self.formLayout1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout1.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout1.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout1.setContentsMargins(1, 1, 1, 2)
        self.formLayout1.setSpacing(10)
        self.formLayout1.setObjectName("formLayout1")
        self.label1 = QtWidgets.QLabel(self.inputGroupBox)
        self.label1.setObjectName("label1")
        self.formLayout1.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label1)
        self.numMeasure = QtWidgets.QLineEdit(self.inputGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numMeasure.sizePolicy().hasHeightForWidth())
        self.numMeasure.setSizePolicy(sizePolicy)
        self.numMeasure.setInputMethodHints(QtCore.Qt.ImhNone)
        self.numMeasure.setMaxLength(3)
        self.numMeasure.setObjectName("numMeasure")
        self.formLayout1.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.numMeasure)
        self.label2 = QtWidgets.QLabel(self.inputGroupBox)
        self.label2.setObjectName("label2")
        self.formLayout1.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label2)
        self.numTreat = QtWidgets.QLineEdit(self.inputGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numTreat.sizePolicy().hasHeightForWidth())
        self.numTreat.setSizePolicy(sizePolicy)
        self.numTreat.setInputMethodHints(QtCore.Qt.ImhNone)
        self.numTreat.setMaxLength(3)
        self.numTreat.setObjectName("numTreat")
        self.formLayout1.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.numTreat)
        self.label3 = QtWidgets.QLabel(self.inputGroupBox)
        self.label3.setObjectName("label3")
        self.formLayout1.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label3)
        self.numBf = QtWidgets.QLineEdit(self.inputGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numBf.sizePolicy().hasHeightForWidth())
        self.numBf.setSizePolicy(sizePolicy)
        self.numBf.setInputMethodHints(QtCore.Qt.ImhNone)
        self.numBf.setMaxLength(3)
        self.numBf.setObjectName("numBf")
        self.formLayout1.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.numBf)
        self.label4 = QtWidgets.QLabel(self.inputGroupBox)
        self.label4.setObjectName("label4")
        self.formLayout1.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label4)
        self.nameMeas = QtWidgets.QLineEdit(self.inputGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameMeas.sizePolicy().hasHeightForWidth())
        self.nameMeas.setSizePolicy(sizePolicy)
        self.nameMeas.setInputMethodHints(QtCore.Qt.ImhNone)
        self.nameMeas.setMaxLength(30)
        self.nameMeas.setObjectName("nameMeas")
        self.formLayout1.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.nameMeas)
        self.label5 = QtWidgets.QLabel(self.inputGroupBox)
        self.label5.setObjectName("label5")
        self.formLayout1.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label5)
        self.namedVar = QtWidgets.QLineEdit(self.inputGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.namedVar.sizePolicy().hasHeightForWidth())
        self.namedVar.setSizePolicy(sizePolicy)
        self.namedVar.setInputMethodHints(QtCore.Qt.ImhNone)
        self.namedVar.setMaxLength(30)
        self.namedVar.setObjectName("namedVar")
        self.formLayout1.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.namedVar)
        self.verticalLayout_1.addLayout(self.formLayout1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.s1but = QtWidgets.QPushButton(self.inputGroupBox)
        self.s1but.setMaximumSize(QtCore.QSize(131, 32))
        self.s1but.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.s1but.setObjectName("s1but")
        self.horizontalLayout.addWidget(self.s1but)
        self.editInputs = QtWidgets.QPushButton(self.inputGroupBox)
        self.editInputs.setMinimumSize(QtCore.QSize(0, 0))
        self.editInputs.setMaximumSize(QtCore.QSize(140, 16777215))
        self.editInputs.setObjectName("editInputs")
        self.horizontalLayout.addWidget(self.editInputs)
        self.verticalLayout_1.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.inputGroupBox)
        self.bFGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.bFGroupBox.setMinimumSize(QtCore.QSize(360, 170))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.bFGroupBox.setFont(font)
        self.bFGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.bFGroupBox.setFlat(False)
        self.bFGroupBox.setCheckable(False)
        self.bFGroupBox.setObjectName("bFGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.bFGroupBox)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bFscrollArea = QtWidgets.QScrollArea(self.bFGroupBox)
        self.bFscrollArea.setMinimumSize(QtCore.QSize(30, 40))
        self.bFscrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bFscrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.bFscrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.bFscrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.bFscrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.bFscrollArea.setWidgetResizable(True)
        self.bFscrollArea.setObjectName("bFscrollArea")
        self.bFscrollWidget = QtWidgets.QWidget()
        self.bFscrollWidget.setGeometry(QtCore.QRect(0, 0, 380, 96))
        self.bFscrollWidget.setObjectName("bFscrollWidget")
        self.bFscrollArea.setWidget(self.bFscrollWidget)
        self.verticalLayout_2.addWidget(self.bFscrollArea)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.s2but = QtWidgets.QPushButton(self.bFGroupBox)
        self.s2but.setMaximumSize(QtCore.QSize(131, 32))
        self.s2but.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.s2but.setObjectName("s2but")
        self.horizontalLayout_2.addWidget(self.s2but)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addWidget(self.bFGroupBox)
        self.errorGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.errorGroupBox.setMinimumSize(QtCore.QSize(360, 75))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.errorGroupBox.setFont(font)
        self.errorGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.errorGroupBox.setFlat(False)
        self.errorGroupBox.setCheckable(False)
        self.errorGroupBox.setObjectName("errorGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.errorGroupBox)
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.eRscrollArea = QtWidgets.QScrollArea(self.errorGroupBox)
        self.eRscrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.eRscrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.eRscrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eRscrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.eRscrollArea.setWidgetResizable(True)
        self.eRscrollArea.setObjectName("eRscrollArea")
        self.eRscrollWidget = QtWidgets.QWidget()
        self.eRscrollWidget.setGeometry(QtCore.QRect(0, 0, 380, 103))
        self.eRscrollWidget.setObjectName("eRscrollWidget")
        self.eRscrollArea.setWidget(self.eRscrollWidget)
        self.verticalLayout_3.addWidget(self.eRscrollArea)
        self.verticalLayout_5.addWidget(self.errorGroupBox)
        self.tGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.tGroupBox.setMinimumSize(QtCore.QSize(360, 180))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.tGroupBox.setFont(font)
        self.tGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tGroupBox.setFlat(False)
        self.tGroupBox.setCheckable(False)
        self.tGroupBox.setObjectName("tGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tGroupBox)
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tScrollArea = QtWidgets.QScrollArea(self.tGroupBox)
        self.tScrollArea.setMinimumSize(QtCore.QSize(0, 40))
        self.tScrollArea.setWidgetResizable(True)
        self.tScrollArea.setObjectName("tScrollArea")
        self.tScrollWidget = QtWidgets.QWidget()
        self.tScrollWidget.setGeometry(QtCore.QRect(0, 0, 396, 106))
        self.tScrollWidget.setObjectName("tScrollWidget")
        self.tScrollArea.setWidget(self.tScrollWidget)
        self.verticalLayout_4.addWidget(self.tScrollArea)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.s4but = QtWidgets.QPushButton(self.tGroupBox)
        self.s4but.setMaximumSize(QtCore.QSize(131, 32))
        self.s4but.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.s4but.setObjectName("s4but")
        self.horizontalLayout_3.addWidget(self.s4but)
        self.updates4 = QtWidgets.QPushButton(self.tGroupBox)
        self.updates4.setObjectName("updates4")
        self.horizontalLayout_3.addWidget(self.updates4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5.addWidget(self.tGroupBox)
        self.horizontalLayout_11.addLayout(self.verticalLayout_5)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.dGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.dGroupBox.setMinimumSize(QtCore.QSize(360, 160))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.dGroupBox.setFont(font)
        self.dGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.dGroupBox.setFlat(False)
        self.dGroupBox.setCheckable(False)
        self.dGroupBox.setObjectName("dGroupBox")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.dGroupBox)
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.dScrollArea = QtWidgets.QScrollArea(self.dGroupBox)
        self.dScrollArea.setMinimumSize(QtCore.QSize(0, 380))
        self.dScrollArea.setWidgetResizable(True)
        self.dScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.dScrollArea.setObjectName("dScrollArea")
        self.dScrollWidget = QtWidgets.QWidget()
        self.dScrollWidget.setGeometry(QtCore.QRect(0, 0, 454, 378))
        self.dScrollWidget.setObjectName("dScrollWidget")
        self.dScrollArea.setWidget(self.dScrollWidget)
        self.verticalLayout_6.addWidget(self.dScrollArea)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.s5but = QtWidgets.QPushButton(self.dGroupBox)
        self.s5but.setMaximumSize(QtCore.QSize(170, 16777215))
        self.s5but.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.s5but.setObjectName("s5but")
        self.horizontalLayout_5.addWidget(self.s5but)
        self.loadgridCSV = QtWidgets.QPushButton(self.dGroupBox)
        self.loadgridCSV.setMaximumSize(QtCore.QSize(160, 16777215))
        self.loadgridCSV.setObjectName("loadgridCSV")
        self.horizontalLayout_5.addWidget(self.loadgridCSV)
        self.autogenGrid = QtWidgets.QPushButton(self.dGroupBox)
        self.autogenGrid.setObjectName("autogenGrid")
        self.horizontalLayout_5.addWidget(self.autogenGrid)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.addRun = QtWidgets.QPushButton(self.dGroupBox)
        self.addRun.setMaximumSize(QtCore.QSize(132, 16777215))
        self.addRun.setObjectName("addRun")
        self.horizontalLayout_4.addWidget(self.addRun)
        self.numRuns = QtWidgets.QLineEdit(self.dGroupBox)
        self.numRuns.setMaximumSize(QtCore.QSize(70, 16777215))
        self.numRuns.setMaxLength(3)
        self.numRuns.setObjectName("numRuns")
        self.horizontalLayout_4.addWidget(self.numRuns)
        self.runCount = QtWidgets.QLabel(self.dGroupBox)
        self.runCount.setMaximumSize(QtCore.QSize(155, 16777215))
        self.runCount.setObjectName("runCount")
        self.horizontalLayout_4.addWidget(self.runCount)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.editGrid = QtWidgets.QPushButton(self.dGroupBox)
        self.editGrid.setMaximumSize(QtCore.QSize(160, 16777215))
        self.editGrid.setObjectName("editGrid")
        self.horizontalLayout_6.addWidget(self.editGrid)
        self.exportTextBut = QtWidgets.QPushButton(self.dGroupBox)
        self.exportTextBut.setMaximumSize(QtCore.QSize(120, 16777215))
        self.exportTextBut.setObjectName("exportTextBut")
        self.horizontalLayout_6.addWidget(self.exportTextBut)
        self.glmCalc = QtWidgets.QPushButton(self.dGroupBox)
        self.glmCalc.setMaximumSize(QtCore.QSize(170, 16777215))
        self.glmCalc.setObjectName("glmCalc")
        self.horizontalLayout_6.addWidget(self.glmCalc)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label = QtWidgets.QLabel(self.dGroupBox)
        self.label.setMaximumSize(QtCore.QSize(113, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label)
        self.experimentName = QtWidgets.QLineEdit(self.dGroupBox)
        self.experimentName.setMaximumSize(QtCore.QSize(120, 16777215))
        self.experimentName.setObjectName("experimentName")
        self.horizontalLayout_7.addWidget(self.experimentName)
        self.exportSAS = QtWidgets.QPushButton(self.dGroupBox)
        self.exportSAS.setMaximumSize(QtCore.QSize(210, 16777215))
        self.exportSAS.setObjectName("exportSAS")
        self.horizontalLayout_7.addWidget(self.exportSAS)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.verticalLayout_6.addLayout(self.verticalLayout)
        self.verticalLayout_7.addWidget(self.dGroupBox)
        self.cGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.cGroupBox.setMinimumSize(QtCore.QSize(360, 150))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.cGroupBox.setFont(font)
        self.cGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.cGroupBox.setFlat(False)
        self.cGroupBox.setCheckable(False)
        self.cGroupBox.setObjectName("cGroupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.cGroupBox)
        self.verticalLayout_8.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.cScrollArea = QtWidgets.QScrollArea(self.cGroupBox)
        self.cScrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.cScrollArea.setWidgetResizable(True)
        self.cScrollArea.setObjectName("cScrollArea")
        self.cScrollWidget = QtWidgets.QWidget()
        self.cScrollWidget.setGeometry(QtCore.QRect(0, 0, 454, 118))
        self.cScrollWidget.setObjectName("cScrollWidget")
        self.cScrollArea.setWidget(self.cScrollWidget)
        self.verticalLayout_8.addWidget(self.cScrollArea)
        self.verticalLayout_7.addWidget(self.cGroupBox)
        self.horizontalLayout_11.addLayout(self.verticalLayout_7)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.GLMGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.GLMGroupBox.setMinimumSize(QtCore.QSize(360, 500))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.GLMGroupBox.setFont(font)
        self.GLMGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.GLMGroupBox.setFlat(False)
        self.GLMGroupBox.setCheckable(False)
        self.GLMGroupBox.setObjectName("GLMGroupBox")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.GLMGroupBox)
        self.verticalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_9.setSpacing(2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.FscrollArea = QtWidgets.QScrollArea(self.GLMGroupBox)
        self.FscrollArea.setMinimumSize(QtCore.QSize(0, 80))
        self.FscrollArea.setMaximumSize(QtCore.QSize(16777215, 145))
        self.FscrollArea.setWidgetResizable(True)
        self.FscrollArea.setObjectName("FscrollArea")
        self.FScrollWidget = QtWidgets.QWidget()
        self.FScrollWidget.setGeometry(QtCore.QRect(0, 0, 396, 78))
        self.FScrollWidget.setObjectName("FScrollWidget")
        self.FscrollArea.setWidget(self.FScrollWidget)
        self.verticalLayout_9.addWidget(self.FscrollArea)
        self.GLMScrollArea = QtWidgets.QScrollArea(self.GLMGroupBox)
        self.GLMScrollArea.setMinimumSize(QtCore.QSize(0, 335))
        self.GLMScrollArea.setWidgetResizable(True)
        self.GLMScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.GLMScrollArea.setObjectName("GLMScrollArea")
        self.GLMScrollWidget = QtWidgets.QWidget()
        self.GLMScrollWidget.setGeometry(QtCore.QRect(0, 0, 396, 333))
        self.GLMScrollWidget.setObjectName("GLMScrollWidget")
        self.GLMScrollArea.setWidget(self.GLMScrollWidget)
        self.verticalLayout_9.addWidget(self.GLMScrollArea)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.parsepower = QtWidgets.QPushButton(self.GLMGroupBox)
        self.parsepower.setMaximumSize(QtCore.QSize(190, 16777215))
        self.parsepower.setObjectName("parsepower")
        self.horizontalLayout_8.addWidget(self.parsepower)
        self.verticalLayout_10.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.exportpwrcsv = QtWidgets.QPushButton(self.GLMGroupBox)
        self.exportpwrcsv.setMaximumSize(QtCore.QSize(250, 16777215))
        self.exportpwrcsv.setObjectName("exportpwrcsv")
        self.horizontalLayout_9.addWidget(self.exportpwrcsv)
        self.verticalLayout_10.addLayout(self.horizontalLayout_9)
        self.verticalLayout_9.addLayout(self.verticalLayout_10)
        self.verticalLayout_12.addWidget(self.GLMGroupBox)
        self.PCGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.PCGroupBox.setMinimumSize(QtCore.QSize(360, 115))
        self.PCGroupBox.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.PCGroupBox.setFont(font)
        self.PCGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.PCGroupBox.setFlat(False)
        self.PCGroupBox.setCheckable(False)
        self.PCGroupBox.setObjectName("PCGroupBox")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.PCGroupBox)
        self.verticalLayout_11.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_11.setSpacing(2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.PCScrollArea = QtWidgets.QScrollArea(self.PCGroupBox)
        self.PCScrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.PCScrollArea.setWidgetResizable(True)
        self.PCScrollArea.setObjectName("PCScrollArea")
        self.PCScrollWidget = QtWidgets.QWidget()
        self.PCScrollWidget.setGeometry(QtCore.QRect(0, 0, 396, 148))
        self.PCScrollWidget.setObjectName("PCScrollWidget")
        self.PCScrollArea.setWidget(self.PCScrollWidget)
        self.verticalLayout_11.addWidget(self.PCScrollArea)
        self.verticalLayout_12.addWidget(self.PCGroupBox)
        self.horizontalLayout_11.addLayout(self.verticalLayout_12)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setAutoFillBackground(True)
        self.statusBar.setStyleSheet("background-color: none;")
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1350, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuSession = QtWidgets.QMenu(self.menuBar)
        self.menuSession.setObjectName("menuSession")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionSave_2 = QtWidgets.QAction(MainWindow)
        self.actionSave_2.setObjectName("actionSave_2")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.menuSession.addAction(self.actionSave)
        self.menuSession.addAction(self.actionReset)
        self.menuSession.addAction(self.actionSave_2)
        self.menuSession.addAction(self.actionLoad)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuBar.addAction(self.menuSession.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Modeler"))
        self.inputGroupBox.setTitle(_translate("MainWindow", "Step 1 - Enter Inputs:"))
        self.label1.setText(_translate("MainWindow", "Total measurements:"))
        self.numMeasure.setPlaceholderText(_translate("MainWindow", "Enter value"))
        self.label2.setText(_translate("MainWindow", "Number of treatments:"))
        self.numTreat.setPlaceholderText(_translate("MainWindow", "Enter value"))
        self.label3.setText(_translate("MainWindow", "Number of blocking factors:"))
        self.numBf.setPlaceholderText(_translate("MainWindow", "Enter value"))
        self.label4.setText(_translate("MainWindow", "Name of measurement:"))
        self.nameMeas.setPlaceholderText(_translate("MainWindow", "Enter name"))
        self.label5.setText(_translate("MainWindow", "Name of dependent variable:"))
        self.namedVar.setPlaceholderText(_translate("MainWindow", "Enter name"))
        self.s1but.setText(_translate("MainWindow", "Continue"))
        self.editInputs.setText(_translate("MainWindow", "Edit inputs"))
        self.bFGroupBox.setTitle(_translate("MainWindow", "Step 2 - Enter blocking factor labels and values:"))
        self.s2but.setText(_translate("MainWindow", "Continue"))
        self.errorGroupBox.setTitle(_translate("MainWindow", "Step 3 - Enter Errors:"))
        self.tGroupBox.setTitle(_translate("MainWindow", "Step 4 - Enter treatment means and labels (optional):"))
        self.s4but.setText(_translate("MainWindow", "Continue"))
        self.updates4.setText(_translate("MainWindow", "Update Error/Treatment Means"))
        self.dGroupBox.setTitle(_translate("MainWindow", "Step 5 - Distribute groups:"))
        self.s5but.setText(_translate("MainWindow", "Generate values"))
        self.loadgridCSV.setText(_translate("MainWindow", "Load in grid CSV"))
        self.autogenGrid.setText(_translate("MainWindow", "Auto-gen grid"))
        self.addRun.setText(_translate("MainWindow", "Add run"))
        self.numRuns.setPlaceholderText(_translate("MainWindow", "# of runs"))
        self.runCount.setText(_translate("MainWindow", "Current run count: 0"))
        self.editGrid.setText(_translate("MainWindow", "Edit grid distribution"))
        self.exportTextBut.setText(_translate("MainWindow", "Export run(s)"))
        self.glmCalc.setText(_translate("MainWindow", "Run GLM calculations"))
        self.label.setText(_translate("MainWindow", "Experiment Name:"))
        self.experimentName.setPlaceholderText(_translate("MainWindow", "Enter name"))
        self.exportSAS.setText(_translate("MainWindow", "Export SAS run(s) to text file"))
        self.cGroupBox.setTitle(_translate("MainWindow", "Current Inputs:"))
        self.GLMGroupBox.setTitle(_translate("MainWindow", "General Linear Model - F-test and pairwise t-test output:"))
        self.parsepower.setText(_translate("MainWindow", "Parse and estimate power"))
        self.exportpwrcsv.setText(_translate("MainWindow", "Export pairwise t-test results to CSV"))
        self.PCGroupBox.setTitle(_translate("MainWindow", "Power estimation calculation and results:"))
        self.menuSession.setTitle(_translate("MainWindow", "Session"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSave.setText(_translate("MainWindow", "Save to Excel"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        self.actionSave_2.setText(_translate("MainWindow", "Dump to JSON"))
        self.actionLoad.setText(_translate("MainWindow", "Load from JSON"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
