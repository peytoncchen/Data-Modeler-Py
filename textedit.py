#Customized QLineEdit widget to be used throughout app

from PyQt5.QtWidgets import *

class TextEdit(QLineEdit):
    def __init__(self):
        super(TextEdit, self).__init__()
        self.setMaxLength(10)
        self.setPlaceholderText("Enter value")
        self.setFixedWidth(80)
        #self.setStyleSheet("margin: 1px; padding: 10px; \
                               #border-style: solid; \
                               #border-radius: 8px; \
                               #border-width: 1px; \
                               #border-color: \
                               #gray;")