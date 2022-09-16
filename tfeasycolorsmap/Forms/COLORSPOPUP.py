from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from ..Core.KRITA import *
from ..UI.ColorsMapRender import *
from ..UI.QColorsMap import *

class COLORSPOPUP(QWidget):
    def __init__(self):
        super().__init__()
        self.fileName = ""
        self.map = list()

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("TF Easy Colors Map")
        self.resize(240, 320)  

        self.colorsMap = QLabel()
        self.colorsMap.mousePressEvent = self.onColorsMapClick
        self.colorsMap.setCursor(KRITA.cursor('krita_tool_color_sampler'))

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
        rendered =  ColorsMapRender.run(self.fileName, self.scrollArea, True)
        self.colorsMap.setPixmap(rendered["pixmap"])
        self.map = rendered["map"]

    def resizeEvent(self, event):
        self.renderFile()

    def onColorsMapClick(self, event):
        click = KRITA.getEvent(event)

        # LEFT CLICK
        if (click["left"]):
            foundItem = QColorsMap.findItemIndex(click["x"], click["y"])
            if (foundItem["index"] < 0): return

            if (foundItem["isColor"]):
                # COLOR
                if (click["noModifier"]):
                    KRITA.setColor("F", QColorsMap.createColorFromMap(foundItem["index"]))
                elif (click["isShift"]):
                    KRITA.setColor("B", QColorsMap.createColorFromMap(foundItem["index"]))

        self.close()
        pass
    