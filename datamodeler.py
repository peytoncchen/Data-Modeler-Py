# Data Modeler for Power Calculations Python Edition

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from textedit import TextEdit


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Data Modeler")
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        textfield = TextEdit()
        text = QLabel("Placeholder")
        layout.addWidget(textfield)
        layout.addWidget(text)


        textfield.returnPressed.connect(self.return_pressed)
        textfield.selectionChanged.connect(self.selection_changed)
        textfield.textChanged.connect(self.text_changed)
        textfield.textEdited.connect(self.text_edited)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        
    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())
        
    def text_changed(self, s):
        print("Text changed...")
        print(s)
            
    def text_edited(self, s):
        print("Text edited...")
        print(s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(700, 300)
    window.show()

    sys.exit(app.exec_())
