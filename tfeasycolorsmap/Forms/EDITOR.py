from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from ..Core.FILE import *
from ..UI.Tools import *

class EDITOR(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.fileName = ""

        self.setFixedWidth(640)    
        self.setFixedHeight(480)    
        self.setWindowTitle("TF Easy Colors Map » EDITOR")

        self.textArea = QPlainTextEdit(self)
        self.textArea.setWordWrapMode(QTextOption.NoWrap)
        
        layout.addWidget(self.textArea)
        layout.addWidget(Tools.bt("SAVE", self.save))
        self.setLayout(layout)

    def read(self, fileName):
        self.fileName = fileName
        self.textArea.setPlainText(FILE.openText(fileName))

    def save(self):
        FILE.save(self.fileName, self.textArea.toPlainText())
        self.close()

