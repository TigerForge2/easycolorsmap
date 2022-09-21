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
        self.t3 = QLineEdit()
        
        self.fileName = ""

        self.setFixedWidth(560)    
        self.setWindowTitle("TF Easy Colors Map » SETTINGS")

        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()
        l5 = QLabel()
        l6 = QLabel()
        l7 = QLabel()
        l8 = QLabel()
        
        l1 = self.title(l1, "Color size")
        l2 = self.desc(l2, "Set the size of the Color boxes. Size must be a value from 24 to 96 (42 by default).")

        l3 = self.title(l3, "Color Name size")
        l4 = self.desc(l4, "Set the size of the Color name inside a box. Size must be a value from 8 to 18 (10 by default).")

        l7 = self.title(l7, "Groups color")
        l8 = self.desc(l8, "Set the colors for the Background and the Text of the Groups. The two colors must be typed\nas HTML colors, separated by a space (e.g. #000000 #FFFFFF -> black background, white text).")

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
        formLayout.layout().addWidget(l7)
        formLayout.layout().addWidget(l8)
        formLayout.layout().addWidget(self.t3)
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
        groupColors = self.t3.text()

        if (colorSize < 24 or colorSize > 96):
            ALERT.error("INVALID SIZE", "The entered 'Color size' is not valid. You have to type values from 24 to 96.")
            return

        if (colorFontSize < 8 or colorFontSize > 18):
            ALERT.error("INVALID SIZE", "The entered 'Color Name size' is not valid. You have to type values from 8 to 18.")
            return

        if (len(groupColors) < 15):
            ALERT.info("INVALID COLORS", "The 'Groups color' field is empty (or not valid) and it will be filled with default values.\n\nChange that colors if you prefer something different.")
            self.t3.setText("#000000 #FFFFFF")
            return

        self.saveToFile(colorSize, colorFontSize, groupColors)   

    def saveDefaults(self):
        self.saveToFile(42, 10)       

    # Save the given two values and close the form.
    def saveToFile(self, colorSize, fontSize, groupColors):
        fileContent = FILE.open(self.fileName)

        fileContent[0] = FILE.changeLineValue(fileContent[0], 6, str(colorSize))
        fileContent[0] = FILE.changeLineValue(fileContent[0], 8, str(fontSize))
        fileContent[0] = FILE.changeLineValue(fileContent[0], 11, groupColors)

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
        self.t3.setText(data[11])

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
