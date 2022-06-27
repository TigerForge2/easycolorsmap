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
            px = self.colorsMapImage.pixelColor(x, y)
            if (not modifierPressed):
                self.changeKritaColor(px, 0)
            elif (isShift):
                self.changeKritaColor(px, 1)

        self.close()
        pass

    def changeKritaColor(self, px, type):
        myColor = UI.getManagedColor(px)
        if (type == 0): 
            UI.setForeGroundColor(myColor) 
        else: 
            UI.setBackGroundColor(myColor)
        pass

