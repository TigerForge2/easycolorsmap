from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from krita import *
from .FILE import *
from .UI import *
from .SYS import *

class POPUP(QWidget):
    def __init__(self):
        super().__init__()
        self.fileName = ""
        self.map = list()

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("TF Easy Colors Map")
        self.resize(240, 320)  

        self.colorsMap = QLabel()
        self.colorsMap.mousePressEvent = self.onColorsMapClick
        self.colorsMap.setCursor(UI.getCursor('krita_tool_color_sampler'))
        self.colorsMapImage = QImage()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.colorsMap)

        layout = QVBoxLayout()
        layout.layout().addWidget(self.scrollArea)

        self.setLayout(layout)

    def read(self, fileName):
        if fileName != "":
            self.fileName = fileName
            self.colorsMap.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.renderFile(True)

    def renderFile(self, resize = False):
        rendered = UI.renderColorsMap(self.fileName, self.scrollArea.size())
        self.colorsMap.setPixmap(rendered["pixmap"])
        self.map = rendered["map"]
        self.colorsMapImage = self.colorsMap.pixmap().toImage()

    def resizeEvent(self, event):
        self.renderFile()

    def onColorsMapClick(self, event):
        modifierPressed = QApplication.keyboardModifiers()
        isShift = (modifierPressed & Qt.ShiftModifier)
        isCtrl = (modifierPressed & Qt.ControlModifier)
        isAlt = (modifierPressed & Qt.AltModifier)
        leftClick = (event.buttons() == Qt.LeftButton)
        rightClick = (event.buttons() == Qt.RightButton)

        x = event.pos().x() - 8
        y = event.pos().y() + 8

        if (leftClick):
            itemIndex = self.getClickedItemIndex(x, y)
            if (not modifierPressed):
                self.changeKritaColor(itemIndex, 0)
            elif (isShift):
                self.changeKritaColor(itemIndex, 1)

        self.close()
        pass

    def changeKritaColor(self, index, type):
        if (index < 0): return

        fileColor = UI.getColorFromIndex(self.fileName, index)
        data = fileColor.split("|")
        myColor = UI.getManagedColor(float(data[1]), float(data[2]), float(data[3]), float(data[4]))
        self.setKritaColor(type, myColor)

    def setKritaColor(self, type, managedColor):
        if (type == 0): 
            UI.setForeGroundColor(managedColor) 
        else: 
            UI.setBackGroundColor(managedColor)

    def getClickedItemIndex(self, x, y):
        for index, item in enumerate(self.map):
            tmp = item.split("|")
            itemIndex = int(tmp[0])
            itemType = tmp[1]
            X1 = int(tmp[2])
            Y1 = int(tmp[3])
            itemW = int(tmp[4])
            itemH = int(tmp[5])
            
            X2 = X1 + itemW
            Y2 = Y1 + itemH

            if (x >= X1 and x <= X2 and y >= Y1 and y <= Y2): return itemIndex

        return -1

