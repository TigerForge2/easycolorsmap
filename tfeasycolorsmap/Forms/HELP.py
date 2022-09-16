from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from ..Core.FILE import *
from ..Core.ALERT import *

class HELP(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.fileName = ""

        self.setFixedWidth(640)    
        self.setFixedHeight(480)    
        self.setWindowTitle("TF Easy Colors Map » GUIDE")

        self.textArea = QTextEdit(self)
        self.textArea.setReadOnly(True)
        self.textArea.setHtml("")
        
        layout.addWidget(self.textArea)
        self.setLayout(layout)

    def init(self):
        fileName = FILE.getCurrentPathToFile(__file__, "guide.html")
        html = FILE.openText(fileName)
        self.textArea.setHtml(html)




