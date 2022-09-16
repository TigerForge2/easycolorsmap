from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from ..UI.Tools import *
from ..Core.FILE import *
from ..Core.ALERT import *

class CONFIG(QWidget):
    def __init__(self):
        super().__init__()
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        
        self.fileName = ""

        self.setFixedWidth(560)    
        self.setWindowTitle("TF Easy Colors Map » SETTINGS")

        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()
        l5 = QLabel()
        l6 = QLabel()

        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        
        l1 = self.title(l1, "Color size")
        l2 = self.desc(l2, "Set the size of the Color boxes. Size must be a value from 24 to 96 (42 by default).")

        l3 = self.title(l3, "Color Name size")
        l4 = self.desc(l4, "Set the size of the Color name inside a box. Size must be a value from 8 to 18 (10 by default).")

        l5 = self.title(l5, "\nHide / Show Groups")
        l6 = self.desc(l6, "Check or uncheck the Groups you want to show or hide in the Colors Map view.")

        self.groupsLayout = QListWidget()
        self.groupsLayout.setFixedHeight(160)
        
        formLayout = Tools.QWidgetLayout("V", Qt.AlignLeft | Qt.AlignTop)
        formLayout.layout().addWidget(l1)
        formLayout.layout().addWidget(l2)
        formLayout.layout().addWidget(self.t1)
        formLayout.layout().addWidget(l3)
        formLayout.layout().addWidget(l4)
        formLayout.layout().addWidget(self.t2)
        formLayout.layout().addWidget(l5)
        formLayout.layout().addWidget(l6)
        formLayout.layout().addWidget(self.groupsLayout)

        btsLayout = Tools.QWidgetLayout("H", Qt.AlignRight)
        btsLayout.layout().addWidget(Tools.toolBt("", self.save, "Save and apply all these settings.", Qt.ToolButtonTextOnly, "APPLY"))
        btsLayout.layout().addWidget(Tools.toolBt("", self.saveDefaults, "Save and apply the default settings for Color size and name size.", Qt.ToolButtonTextOnly, "SET DEFAULTS"))
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.layout().addWidget(formLayout)
        self.layout().addWidget(btsLayout)

    def save(self):
        colorSize = int(self.t1.text())
        colorFontSize = int(self.t2.text())

        if (colorSize < 24 or colorSize > 96):
            ALERT.error("INVALID SIZE", "The entered 'Color size' is not valid. You have to type values from 24 to 96.")
            return

        if (colorFontSize < 8 or colorFontSize > 18):
            ALERT.error("INVALID SIZE", "The entered 'Color Name size' is not valid. You have to type values from 8 to 18.")
            return

        self.saveToFile(colorSize, colorFontSize)   

    def saveDefaults(self):
        self.saveToFile(42, 10)       

    # Save the given two values and close the form.
    def saveToFile(self, colorSize, fontSize):
        fileContent = FILE.open(self.fileName)

        fileContent[0] = FILE.changeLineValue(fileContent[0], 6, str(colorSize))
        fileContent[0] = FILE.changeLineValue(fileContent[0], 8, str(fontSize))

        visibles = ""
        for i in range(self.groupsLayout.count()):
            item = self.groupsLayout.item(i)
            if (item.checkState() == Qt.Checked): visibles += "|" + item.text() + "|"

        for index, line in enumerate(fileContent):
            if (line.find("[G]") == 0):
                groupName = "|" + FILE.getLineValue(line, 3) + "|"
                if (visibles.find(groupName) >= 0):
                    fileContent[index] = FILE.changeLineValue(line, 2, "[V]")
                else:
                    fileContent[index] = FILE.changeLineValue(line, 2, "[-]")

        FILE.saveList(self.fileName, fileContent)
        self.close()

    

    def init(self, fileName):
        self.fileName = fileName
        data = FILE.extractLine(fileName, 0).split("|")

        self.t1.setText(data[6])
        self.t2.setText(data[8])

        self.groupsLayout.clear()

        groups = FILE.getGroupsList(self.fileName)
        for line in groups:
            data = line.split("|")

            item = QListWidgetItem(data[3], self.groupsLayout)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if data[2] == "[V]" else Qt.Unchecked)
            self.groupsLayout.addItem(item)

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
