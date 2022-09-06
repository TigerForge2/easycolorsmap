from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from krita import *
from .FILE import *
from .UI import *
from .SYS import *

class CONFIG(QWidget):
    def __init__(self):
        super().__init__()
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        
        self.fileName = ""

        self.setFixedWidth(560)    
        #self.setFixedHeight(240)    
        self.setWindowTitle("TF Easy Colors Map » SETTINGS")

        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()

        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        
        l1 = self.title(l1, "Color size")
        l2 = self.desc(l2, "Set the size of the Color boxes. Size must be a value from 32 to 64 (42 by default).")

        l3 = self.title(l3, "Color Name size")
        l4 = self.desc(l4, "Set the size of the Color name inside a box. Size must be a value from 8 to 14 (10 by default).")
        
        formLayout = UI.createQWidgetLayout("V", Qt.AlignLeft | Qt.AlignTop)
        formLayout.layout().addWidget(l1)
        formLayout.layout().addWidget(l2)
        formLayout.layout().addWidget(self.t1)
        formLayout.layout().addWidget(l3)
        formLayout.layout().addWidget(l4)
        formLayout.layout().addWidget(self.t2)

        # groupsLayout = UI.createQWidgetLayout("V", Qt.AlignLeft | Qt.AlignTop)
        # groups = UI.getGroupsList(self.fileName)
        # for index, groupName in enumerate(groups):
        #     cb = QCheckBox(groupName)
        #     cb.setFixedHeight(24)
        #     cb.setStyleSheet("QCheckBox::indicator {subcontrol-position: left top;}")
        #     groupsLayout.layout().addWidget(cb)

        btsLayout = UI.createQWidgetLayout("H", Qt.AlignRight)
        btsLayout.layout().addWidget(UI.toolBt("", self.save, "Save and apply these settings.", Qt.ToolButtonTextOnly, "APPLY"))
        btsLayout.layout().addWidget(UI.toolBt("", self.saveDefaults, "Save and apply the default settings.", Qt.ToolButtonTextOnly, "SET DEFAULTS"))

        # for i in reversed(range(self.layout().count())): 
        #     self.layout().itemAt(i).widget().deleteLater()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.layout().addWidget(formLayout)
        #self.layout().addWidget(groupsLayout)
        self.layout().addWidget(btsLayout)

    def save(self):
        colorSize = int(self.t1.text())
        colorFontSize = int(self.t2.text())

        if (colorSize < 32 or colorSize > 64):
            ALERT.error("INVALID SIZE", "The entered 'Color size' is not valid. You have to type values from 32 to 64.")
            return

        if (colorFontSize < 8 or colorFontSize > 14):
            ALERT.error("INVALID SIZE", "The entered 'Color Name size' is not valid. You have to type values from 8 to 14.")
            return

        SYS.config["colorSize"] = colorSize
        SYS.config["colorFontSize"] = colorFontSize
        SYS.configUpdate(self.fileName)
        self.close()
        pass

    def saveDefaults(self):
        SYS.config["colorSize"] = 42
        SYS.config["colorFontSize"] = 10
        SYS.configUpdate(self.fileName)
        self.close()
        pass

    def init(self, fileName):
        self.fileName = fileName
        self.t1.setText(str(SYS.config["colorSize"]))
        self.t2.setText(str(SYS.config["colorFontSize"]))
        self.createUI()

    def createUI(self):
        pass

    def title(self, l1, text):
        l1.setText(text)
        font = l1.font()
        font.setPixelSize(14)
        l1.setFont(font)
        l1.setStyleSheet("font-weight:bold;")
        return l1

    def desc(self, l1, text):
        l1.setText(text)
        font = l1.font()
        l1.setFont(font)
        l1.setStyleSheet("font-style:italic;")
        return l1
