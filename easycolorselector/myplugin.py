from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
from krita import *
from .UI import *
from .ALERT import *
from .FILE import *
from .EDITOR import *
from .HELP import *
import math

class MyDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TF Easy Colors Map")
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
        self.fileName = ""
        self.fileSize = 0
        self.guide = HELP()
        self.editor = EDITOR()
        self.editor.closeEvent = self.editClose
        self.selColor = Qt.black
        self.tempColors = list()
        self.map = list()
        
        openButton = UI.toolBt('document-open', self.fileOpen, "OPEN MAP\nLoad an existing Colors Map or create a new one.")
        editButton = UI.toolBt('document-edit', self.edit, "MAP EDITOR\nEdit the current Colors Map.")
        titleButton = UI.toolBt('draw-text', self.addTitle, "ADD GROUP TITLE\nAdd a title for a group of Colors.")
        self.autoButton = UI.toolBt('fillLayer', self.autoColorAcquisition, "AUTO ADD COLORS\Start/stop the Colors auto-acquisition.")
        self.autoButton.setCheckable(True)
        helpButton = UI.toolBt('document-open', self.help, "GUIDE\nShow the inline guide.", Qt.ToolButtonTextOnly, "?")

        self.contextMenu = QMenu(self)
        self.contextMenuItems = dict()
        self.contextMenuItems["Rename"] = self.contextMenu.addAction("Rename")
        self.contextMenu.addSeparator()
        self.contextMenuItems["Cut"] = self.contextMenu.addAction("Cut")
        self.contextMenuItems["Paste"] = self.contextMenu.addAction("Paste")
        self.contextMenuItems["PasteGroup"] = self.contextMenu.addAction("Paste Group")
        self.contextMenu.addSeparator()
        self.contextMenuItems["Delete"] = self.contextMenu.addAction("Delete")

        self.colorsMap = QLabel(mainWidget)
        self.colorsMap.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.colorsMap.mousePressEvent = self.onColorsMapClick
        self.colorsMap.setCursor(UI.getCursor('krita_tool_color_sampler'))
        self.colorsMapImage = QImage()

        self.tempMap = QLabel(mainWidget)
        self.tempMap.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.tempMap.mousePressEvent = self.onTempMapClick
        self.tempMap.setCursor(UI.getCursor('krita_tool_color_sampler'))
        self.tempMapImage = QImage()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.colorsMap)

        self.scrollTempArea = QScrollArea()
        self.scrollTempArea.setWidgetResizable(True)
        self.scrollTempArea.setWidget(self.tempMap)
        self.scrollTempArea.setStyleSheet("height:16px;max-height:16px")
        self.scrollTempArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.colorLabel = QLabel(mainWidget)
        self.colorLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainWidget.setLayout(mainLayout)

        imageLayout = QWidget()
        iLayout = QVBoxLayout()
        iLayout.setContentsMargins(0, 10, 6, 0)
        imageLayout.setLayout(iLayout)
        imageLayout.layout().addWidget(self.scrollArea)
        imageLayout.layout().addWidget(self.scrollTempArea)

        toolLayout = QWidget()
        tLayout = QHBoxLayout()
        toolLayout.setLayout(tLayout)
        toolLayout.layout().addWidget(openButton)
        toolLayout.layout().addWidget(titleButton)
        toolLayout.layout().addWidget(self.autoButton)
        toolLayout.layout().addWidget(editButton)
        toolLayout.layout().addWidget(self.colorLabel)
        toolLayout.layout().addWidget(helpButton)

        mainWidget.layout().addWidget(imageLayout)
        mainWidget.layout().addWidget(toolLayout)

        self.windowSize = self.scrollArea.size()
        self.timerWindowResize = QTimer()
        self.timerWindowResize.timeout.connect(self.onWindowResize)
        self.timerWindowResize.start(1000)

        self.timerAutoColors = QTimer()
        self.timerAutoColors.timeout.connect(self.autoAddColor)


    def onWindowResize(self):
        if (self.windowSize != self.scrollArea.size()):
            self.windowSize = self.scrollArea.size()
            if (self.fileSize > 0): self.renderFile()
        pass

    def fileOpen(self):
        fileName = ALERT.dialogOpen("Colors Map", "Colors Map Files (*.txt)")
        
        if fileName != "":
            self.fileName = FILE.fileTxt(fileName)
            if (FILE.exists(self.fileName)):
                self.fileSize = UI.getFileSize(self.fileName)
            else:
                self.fileSize = 0      

        self.renderFile()
        pass

    def addTitle(self):
        if (self.fileName != ""):
            title = ALERT.prompt("GROUP TITLE", "Type a title for a new group of Colors:")
            if (title["ok"]):
                FILE.save(self.fileName, title["value"])
                self.renderFile()
        else:
            ALERT.warn("ATTENTION", "There is not a Colors Map file yet.")
        pass

    def autoColorAcquisition(self):
        if (self.autoButton.isChecked()):
            newColor = UI.getForegroundQColor()
            self.selColor = newColor
            self.timerAutoColors.start(1000)
        else:
            self.timerAutoColors.stop()
        pass

    def autoAddColor(self):
        newColor = UI.getForegroundQColor()
        if (newColor != self.selColor):
            self.selColor = newColor
            self.addNewColor()        
        pass

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

        if (rightClick):
            if (not modifierPressed):
                self.addNewColor()
            elif (isShift):
                px = self.colorsMapImage.pixelColor(x, y)
                if (px.alpha() != 0): self.insertNewColor(x, y)
            elif(isCtrl):
                px = self.colorsMapImage.pixelColor(x, y)
                if (px.alpha() != 0):
                    itemIndex = self.getColorIndex(x, y)
                    if (itemIndex >= 0): 
                        action = self.contextMenu.exec_(self.mapToGlobal(event.pos()))
                        FILE.executeAction(action, self.contextMenuItems, itemIndex, self.fileName)
                        self.renderFile()

        pass

    def onTempMapClick(self, event):
        modifierPressed = QApplication.keyboardModifiers()
        isShift = (modifierPressed & Qt.ShiftModifier)
        isCtrl = (modifierPressed & Qt.ControlModifier)
        isAlt = (modifierPressed & Qt.AltModifier)
        leftClick = (event.buttons() == Qt.LeftButton)
        rightClick = (event.buttons() == Qt.RightButton)

        x = event.pos().x() - 8
        y = event.pos().y() + 8

        if (leftClick):
            px = self.tempMapImage.pixelColor(x, y)
            if (not modifierPressed):
                self.changeKritaColor(px, 0)
            elif (isShift):
                self.changeKritaColor(px, 1)

        if (rightClick):
            if (not modifierPressed):
                self.addNewTempColor()

        pass

    def changeKritaColor(self, px, type):
        activeView = Krita.instance().activeWindow().activeView()
        myColor = ManagedColor("RGBA", "U8", "")
        colorComponents = myColor.components()
        colorComponents[0] = px.blueF()
        colorComponents[1] = px.greenF()
        colorComponents[2] = px.redF()
        colorComponents[3] = px.alphaF()
        myColor.setComponents(colorComponents)
        if (type == 0): 
            activeView.setForeGroundColor(myColor) 
        else: 
            activeView.setBackGroundColor(myColor)

        self.colorLabel.setText("RGB  " + str(px.red()) + "  " + str(px.green()) + "  " + str(px.blue()))
        pass

    def addNewColor(self):
        newColor = UI.getForegroundQColor()

        if (newColor):
            self.colorRGBALabel(newColor)
            colorName = ALERT.prompt("NEW COLOR NAME", "Type a short name for this Color:")
            if (colorName["ok"]):
                FILE.save(self.fileName, colorName["value"] + "|" + str(newColor.blueF()) + "|" + str(newColor.greenF()) + "|" + str(newColor.redF()) + "|" + str(newColor.alphaF()) + "|")
                self.fileSize = UI.getFileSize(self.fileName)
                self.renderFile()
        else:
            ALERT.warn("ATTENTION", "You have to open a file in Krita first.")

        pass

    def addNewTempColor(self):
        newColor = UI.getForegroundQColor()
        if (newColor):
            self.tempColors.insert(0, newColor)
            self.renderTemp()
        else:
            ALERT.warn("ATTENTION", "You have to open a file in Krita first.")

        pass

    def renderFile(self):
        if (self.fileSize == 0):
            FILE.write(self.fileName, "NEW COLORS MAP\n")

        rendered = UI.renderColorsMap(self.fileName, self.scrollArea.size())
        self.setPixmap(rendered["pixmap"])
        self.map = rendered["map"]
        pass

    def renderTemp(self):
        self.setTempPixmap(UI.renderTempMap(self.tempColors, self.scrollArea.size()))
        pass

    def colorRGBALabel(self, qColor):
        self.colorLabel.setText("RGB  " + str(qColor.red()) + "  " + str(qColor.green()) + "  " + str(qColor.blue()))
        pass

    def setPixmap(self, pixmap):
        self.colorsMap.setPixmap(pixmap)
        self.colorsMapImage = self.colorsMap.pixmap().toImage()
        pass

    def setTempPixmap(self, pixmap):
        self.tempMap.setPixmap(pixmap)
        self.tempMapImage = self.tempMap.pixmap().toImage()
        pass

    def edit(self):
        if (self.fileName != "" and self.fileSize > 0):
            self.editor.read(self.fileName)
            self.editor.show()
        else:
            ALERT.warn("ATTENTION", "There is not a Colors Map file yet.")

    def editClose(self, event):
        self.renderFile()

    def insertNewColor(self, x, y):
        if (len(self.map) == 0):
            ALERT.warn("ATTENTION", "There is not a Colors Map file yet.")
            return

        itemIndex = self.getColorIndex(x, y)
        if (itemIndex >= 0):
            newColor = UI.getForegroundQColor()

            if (newColor):
                self.colorRGBALabel(newColor)
                colorName = ALERT.prompt("NEW COLOR NAME", "Type a short name for this Color:")
                if (colorName["ok"]):
                    FILE.saveToIndex(self.fileName, colorName["value"] + "|" + str(newColor.blueF()) + "|" + str(newColor.greenF()) + "|" + str(newColor.redF()) + "|" + str(newColor.alphaF()) + "|", itemIndex + 1)
                    self.fileSize = UI.getFileSize(self.fileName)
                    self.renderFile()
            else:
                ALERT.warn("ATTENTION", "You have to open a file in Krita first.")

        pass

    def getColorIndex(self, x, y):
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
        pass

    def help(self):
        self.guide.show()
        pass

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory(
    "myColorDocker", DockWidgetFactoryBase.DockRight, MyDocker))


