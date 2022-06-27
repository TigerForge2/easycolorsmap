from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
from krita import *
from .UI import *
from .ALERT import *
from .FILE import *
from .CONFIG import *
from .EDITOR import *
from .HELP import *
from .SYS import *
from .POPUP import *
import math

class MyDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TF Easy Colors Map v." + SYS.getVersionString())
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
        self.fileName = ""
        self.fileSize = 0
        self.settings = CONFIG()
        self.settings.closeEvent = self.configClose
        self.guide = HELP()
        self.editor = EDITOR()
        self.editor.closeEvent = self.editClose
        self.popup = POPUP()
        self.selColor = Qt.black
        self.tempColors = list()
        self.map = list()
        self.myKritaCanvas = None

        appNotifier  = Krita.instance().notifier()
        appNotifier.setActive(True)
        appNotifier.viewClosed.connect(self.viewClosedEvent)
        appNotifier.viewCreated.connect(self.viewOpenedEvent)
        appNotifier.applicationClosing.connect(self.onAppClose)
        
        openButton = UI.toolBt('document-open', self.fileOpen, "OPEN MAP\nLoad an existing Colors Map or create a new one.")
        editButton = UI.toolBt('document-edit', self.edit, "MAP EDITOR\nEdit the current Colors Map.")
        configButton = UI.toolBt('config-performance', self.config, "SETTINGS\nChange the settings of this Colors Map.")
        self.autoButton = UI.toolBt('fillLayer', self.autoColorAcquisition, "AUTO ADD COLORS\Start/stop the Colors auto-acquisition.")
        self.autoButton.setCheckable(True)
        helpButton = UI.toolBt('document-open', self.help, "GUIDE\nShow the inline guide.", Qt.ToolButtonTextOnly, "?")

        self.contextMenu = UI.contextMenu(self)
        self.contextMenuItems = UI.contextMenuItems(
            self.contextMenu,
            [
                ["AddTitle", "Add Group Title", "Add a Group Title after this clicked Color or Group Title."],
                ["Rename", "Rename [left + CTRL]", "Change the name of the clicked Color or Group Title."],
                ["-"],
                ["Cut", "Cut", "Select the clicked Color or Group Title for the next 'Paste' operation."],
                ["Paste", "Paste after", "Paste the 'cut' element after this clicked Color or Group Title."],
                ["PasteGroup", "Paste Group after", "Paste the 'cut' Group Title and Colors after the clicked Color."],
                ["-"],
                ["Delete", "Delete", "Delete the clicked Color or Group Title (not its Colors)"]
            ])

        self.colorsMap = QLabel(mainWidget)
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
        toolLayout.layout().addWidget(self.autoButton)
        toolLayout.layout().addWidget(editButton)
        toolLayout.layout().addWidget(configButton)
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

        self.timerDocOpened = QTimer()
        self.timerDocOpened.timeout.connect(self.getAnnotation)

    def onWindowResize(self):        
        if (self.windowSize != self.scrollArea.size()):
            self.windowSize = self.scrollArea.size()
            if (self.fileSize > 0): self.renderFile()
        pass

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton and event.modifiers() == Qt.ShiftModifier:
                qwindow = Krita.instance().activeWindow().qwindow()
                target_qobj = qwindow.findChild(QToolButton, "KritaShape/KisToolBrush")
                if (target_qobj.isChecked()):
                    c = UI.get_my_canvas(self.myKritaCanvas["canvas"])
                    pos = c["globalPos"]
                    self.popup.read(self.fileName)
                    self.popup.show()
                    self.popup.move(pos.x(), pos.y())

        return super().eventFilter(object, event)

    def viewClosedEvent(self):
        self.fileName = ""
        self.fileSize = 0
        self.tempColors = list()
        self.map = list()
        self.colorsMapImage = QImage()
        self.tempMapImage = QImage()
        pixmap = QPixmap(1, 1)
        pixmap.fill(Qt.transparent)
        self.colorsMap.setPixmap(pixmap)
        self.tempMap.setPixmap(pixmap)
        self.onAppClose()

    def viewOpenedEvent(self):
        self.timerDocOpened.start(1000)

    def getAnnotation(self):
        fileName = UI.getAnnotation()
        if (fileName != ""): 
            self.fileOpenByName(fileName)
        else:
            self.colorsMap.setText("Click here (or the [OPEN MAP] button below)\nto open an existing Colors Map\nor create a new one.")
            self.colorsMap.setAlignment(Qt.AlignCenter)

        self.timerDocOpened.stop()

    def fileOpen(self):
        if (self.noKritaDoc()): return

        fileName = ALERT.dialogOpen("Colors Map", "Colors Map Files (*.txt)")
        self.fileOpenByName(fileName)
        
        pass

    def fileOpenByName(self, fileName):
        if fileName != "":
            self.fileName = FILE.fileTxt(fileName)
            if (FILE.exists(self.fileName)):
                SYS.checkVersion(self.fileName)
            else:
                SYS.initMap(self.fileName)

            self.colorsMap.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.fileSize = UI.getFileSize(self.fileName)
            self.renderFile()
            UI.setAnnotation(self.fileName)

            self.myKritaCanvas = UI.get_my_canvas()
            if (not self.myKritaCanvas["canvas"] is None): self.myKritaCanvas["canvas"].installEventFilter(self)

    def autoColorAcquisition(self):
        if (self.noKritaDoc()): return

        if (self.fileName == ""):
            ALERT.warn("ATTENTION", "There is not a Colors Map file yet.")
            self.autoButton.setChecked(False)
            self.timerAutoColors.stop()
            return

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
        if (self.noKritaDoc()): return
        if (self.fileName == "" and self.fileSize == 0):
            self.fileOpen()
            return

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
            elif (isCtrl):
                px = self.colorsMapImage.pixelColor(x, y)
                if (px.alpha() != 0):
                    itemIndex = self.getColorIndex(x, y)
                    if (itemIndex >= 0): 
                        FILE.executeAction("[RENAME]", self.contextMenuItems, itemIndex, self.fileName)
                        self.renderFile()

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
        if (self.noKritaDoc()): return
        if (self.fileName == "" and self.fileSize == 0):
            self.fileOpen()
            return

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
        myColor = UI.getManagedColor(px)
        if (type == 0): 
            UI.setForeGroundColor(myColor) 
        else: 
            UI.setBackGroundColor(myColor)

        self.colorRGBALabel(px)
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
        rendered = UI.renderColorsMap(self.fileName, self.scrollArea.size())
        self.setPixmap(rendered["pixmap"])
        self.map = rendered["map"]
        pass

    def renderTemp(self):
        self.setTempPixmap(UI.renderTempMap(self.tempColors, self.scrollArea.size()))
        pass

    def colorRGBALabel(self, qColor):
        if (UI.colorProfile() == "RGB"):
            self.colorLabel.setText("RGB  " + str(qColor.red()) + "  " + str(qColor.green()) + "  " + str(qColor.blue()))
        else:
            self.colorLabel.setText("CMYK  " + str(qColor.cyan()) + "  " + str(qColor.magenta()) + "  " + str(qColor.yellow()) + "  " + str(qColor.black()))
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

    def noKritaDoc(self):
        if (UI.noKritaDoc()):
            ALERT.warn("NO KRITA DOCUMENT", "Open a Krita document before creating or loading a Colors Map.")
            return True
        return False


    def help(self):
        self.guide.show()
        pass

    def config(self):
        if (self.fileName == ""):
            ALERT.warn("ATTENTION", "There is not a Colors Map file yet.")
            return
        self.settings.init(self.fileName)
        self.settings.show()
        pass

    def configClose(self, event):
        self.renderFile()

    def canvasChanged(self, canvas):
        pass

    def onAppClose(self):
        self.popup.close()
        self.settings.close()
        self.guide.close()
        self.editor.close()

Krita.instance().addDockWidgetFactory(DockWidgetFactory(
    "myColorDocker", DockWidgetFactoryBase.DockRight, MyDocker))


