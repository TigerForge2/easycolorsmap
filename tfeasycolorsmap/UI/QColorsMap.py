from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *
import math

from .Tools import *
from .ColorsMapRender import *
from .ColorsMapMenu import *
from ..Core.KRITA import *
from ..Core.ALERT import *
from ..Core.FILE import *
from ..Core.SYS import *

# **** Colors Maps management *********************************************************************

class QColorsMap:
    def __init__(self):
        super().__init__()

    @property
    def fileName(self):
        return self.__fileName
    @fileName.setter
    def fileName(self, value):
        self.__fileName = value

    @property
    def map(self):
        return self.__map
    @map.setter
    def map(self, value):
        self.__map = value

    @property
    def pluginSelf(self):
        return self.__pluginSelf
    @pluginSelf.setter
    def pluginSelf(self, value):
        self.__pluginSelf = value

    @property
    def autoColor(self):
        return self.__autoColor
    @autoColor.setter
    def autoColor(self, value):
        self.__autoColor = value

    @property
    def tempColorsMap(self):
        return self.__tempColorsMap
    @tempColorsMap.setter
    def tempColorsMap(self, value):
        self.__tempColorsMap = value


    # ---- Interface ------------------------------------------------------------------------------

    # UI render.
    def render(mainWidget, pluginSelf):
        QColorsMap.fileName = ""
        QColorsMap.autoColor = None
        QColorsMap.map = list()
        QColorsMap.tempColorsMap = list()
        QColorsMap.pluginSelf = pluginSelf # Reference to plugin's 'self'.

        QColorsMap.colorsMap = QLabel(mainWidget)
        QColorsMap.colorsMap.setCursor(KRITA.cursor('krita_tool_color_sampler'))
        QColorsMap.colorsMap.mousePressEvent = QColorsMap.onColorsMapClick

        QColorsMap.colorLabel = QLabel(mainWidget)
        QColorsMap.colorLabel.setAlignment(Qt.AlignCenter)
        QColorsMap.colorLabel.setText("...")

        QColorsMap.scrollMapArea = QScrollArea()
        QColorsMap.scrollMapArea.setWidgetResizable(True)
        QColorsMap.scrollMapArea.setWidget(QColorsMap.colorsMap)
        QColorsMap.lastScrollMapAreaSize = QColorsMap.scrollMapArea.size()

        QColorsMap.tempMap = QLabel(mainWidget)
        QColorsMap.tempMap.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        QColorsMap.tempMap.setCursor(KRITA.cursor('krita_tool_color_sampler'))
        QColorsMap.tempMap.mousePressEvent = QColorsMap.onTempMapClick

        QColorsMap.scrollTempArea = QScrollArea()
        QColorsMap.scrollTempArea.setWidgetResizable(True)
        QColorsMap.scrollTempArea.setWidget(QColorsMap.tempMap)
        QColorsMap.scrollTempArea.setStyleSheet("height:16px;max-height:16px")
        QColorsMap.scrollTempArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        maps = Tools.QWidgetLayout("V", "", True)
        maps.layout().addWidget(QColorsMap.scrollMapArea)
        maps.layout().addWidget(QColorsMap.colorLabel)
        maps.layout().addWidget(QColorsMap.scrollTempArea)

        QColorsMap.lifeCycleFastTimer = Tools.interval(QColorsMap.lifeCycleFast, 500, True)
        QColorsMap.lifeCycleSlowTimer = Tools.interval(QColorsMap.lifeCycleSlow, 1000, True)

        return maps


    # ---- Colors Map click -----------------------------------------------------------------------
    
    # Click on the main Colors Map.
    # If there's no Map, it asks to open/create a Map file.
    def onColorsMapClick(event):
        if (KRITA.isNotReady()): 
            KRITA.actionTrigger("file_open")
            return

        if (QColorsMap.mapExists()):
            QColorsMap.executeColorsMapOperations(event)
        else:
            QColorsMap.openFileDialog()

    # Ask the user to select or create a Colors Map file.        
    def openFileDialog():
        fileName = ALERT.dialogFileOpen("Colors Map", "Colors Map file (*.cmap)")
        QColorsMap.fileName = QColorsMap.checkFileName(fileName)
        if (QColorsMap.fileName == ""): return

        if (FILE.exists(QColorsMap.fileName)):
            QColorsMap.load()
        else:
            QColorsMap.createNewColorsMapFile()
        KRITA.annotationSet(QColorsMap.fileName)

    # Execute the various Colors Map operations when the user clicks on the Colors Map.
    def executeColorsMapOperations(event):
        click = KRITA.getEvent(event)

        # RIGHT CLICK
        if (click["right"]):
            if (click["noModifier"]):
                QColorsMap.newColorAdd()
            elif (click["isShift"]):
                foundItem = QColorsMap.findItemIndex(click["x"], click["y"])
                if (foundItem["index"] >= 0): QColorsMap.newColorAdd(foundItem["index"] + 1)
            elif (click["isCtrl"]):
                foundItem = QColorsMap.findItemIndex(click["x"], click["y"])
                if (foundItem["index"] >= 0): ColorsMapMenu.show(click["globalPos"], foundItem["index"], QColorsMap.fileName)
            QColorsMap.load()

        # LEFT CLICK
        if (click["left"]):
            foundItem = QColorsMap.findItemIndex(click["x"], click["y"])
            if (foundItem["index"] < 0): return

            if (click["isCtrl"]):
                ColorsMapMenu.execute("Rename", foundItem["index"], QColorsMap.fileName)
                QColorsMap.load()
            else:
                if (foundItem["isColor"]):
                    # COLOR
                    if (click["noModifier"]):
                        KRITA.setColor("F", QColorsMap.createColorFromMap(foundItem["index"]))
                    elif (click["isShift"]):
                        KRITA.setColor("B", QColorsMap.createColorFromMap(foundItem["index"]))
                else:
                    # GROUP
                    if (foundItem["isCollapse"]):
                        FILE.modifyLineToggle(QColorsMap.fileName, foundItem["index"], 1, "[O]", "[X]")
                        QColorsMap.load()

            

    # Add a new color to the Colors Map. If index = 0 (default) it's added to the end, otherwise it's added after the given index.
    def newColorAdd(index = 0):
        newColor = KRITA.getSelectedColor("F")
        colorName = ALERT.prompt("NEW COLOR NAME", "Type a short name for this new " + KRITA.colorParam("MODEL") + " Color:")
        if (colorName["ok"]):
            data = "[C]|[O]|[V]|" + colorName["value"] + "|" + KRITA.colorParam("MODEL") + "|" + KRITA.colorParam("DEPTH") + "|" + KRITA.colorParam("PROFILE") + "|"
            for value in newColor: data += value + "|"
            if (index == 0):
                FILE.append(QColorsMap.fileName, data)
            else:
                FILE.saveToIndex(QColorsMap.fileName, data, index)

    # ---- Colors Map render ----------------------------------------------------------------------

    # Graphically render the Colors Map on the QColorsMap widget.
    def colorsMapRender():
        canvas = KRITA.getCurrentCanvas()
        if (not canvas["canvas"] is None): canvas["canvas"].installEventFilter(QColorsMap.pluginSelf)

        data = ColorsMapRender.run(QColorsMap.fileName, QColorsMap.scrollMapArea)
        QColorsMap.colorsMap.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        QColorsMap.colorsMap.setPixmap(data["pixmap"])
        
        # This special 'map' is used for finding the index of an item inside the Colors Map
        QColorsMap.map = data["map"]

    # Return the index (1..n) and type (isColor, isGroup) of an item into the Colors Map file. It requires the QColorsMap.map property correctly filled and the click x/y coordinates.
    def findItemIndex(x, y):
        for index, item in enumerate(QColorsMap.map):
            tmp = item.split("|")
            itemIndex = int(tmp[0])
            itemType = tmp[1]
            X1 = int(tmp[2])
            Y1 = int(tmp[3])
            itemW = int(tmp[4])
            itemH = int(tmp[5])
            
            X2 = X1 + itemW
            Y2 = Y1 + itemH

            isCollapse = False
            if (itemType == "G"):
                cX1 = itemW - 16
                cY1 = Y1
                cX2 = cX1 + 16
                cY2 = cY1 + 16
                if (x >= cX1 and x <= cX2 and y >= cY1 and y <= cY2): isCollapse = True
                
            if (x >= X1 and x <= X2 and y >= Y1 and y <= Y2): return { "index": itemIndex + 1, "isColor": itemType == "C", "isGroup": itemType == "G", "isCollapse": isCollapse }

        return { "index": -1, "type": "" }



    # ---- Colors Map file ------------------------------------------------------------------------

    # Start the creation of a new Colors Map file.
    def createNewColorsMapFile():
        color = KRITA.colorConfig()

        data = ""
        data += "TF Easy Colors Map|2|" + str(SYS.version) + "|" + color["model"] + "|" + color["depth"] + "|" + color["profile"] + "|"
        data += "42|24|10|16|16|" + "\n" # colorSize, titleSize, colorFontSize, titleFontSize, scrollSize
        data += "[G]|[O]|[V]|NEW COLOURS GROUP|" + "\n"

        FILE.save(QColorsMap.fileName, data)
        QColorsMap.load()

    # Open an existing Colors Map file and render the Map.
    def load():
        QColorsMap.colorsMapRender()


    # ---- Life Cycles ----------------------------------------------------------------------------

    # Perform various operation, in the meantime that Krita is opened, which must be executed pretty fast.
    def lifeCycleFast():
        try:
            if (KRITA.isNotReady()): QColorsMap.showStartInstructions(True)
            if (KRITA.isReady() and not QColorsMap.mapExists()): QColorsMap.showMapInstructions(True)

            if (KRITA.isReady() and QColorsMap.mapExists()):
                # Krita app has an opened document and a Colors Map has been loaded / created
                if (QColorsMap.lastScrollMapAreaSize != QColorsMap.scrollMapArea.size()):
                    QColorsMap.lastScrollMapAreaSize = QColorsMap.scrollMapArea.size()
                    QColorsMap.load()
        except:
            pass

    # Perform various operation, in the meantime that Krita is opened, which must be executed pretty slow.
    def lifeCycleSlow():
        try:
            if (KRITA.isReady()):

                # Krita Document annotation management
                annotation = KRITA.annotationGet()
                if (annotation != ""):
                    if (annotation != QColorsMap.fileName):
                        QColorsMap.fileName = annotation
                        QColorsMap.load()
                else:
                    if (QColorsMap.fileName != ""): QColorsMap.reset()

                # Auto-Color feature
                if (not QColorsMap.autoColor is None):
                    currentColor = KRITA.getSelectedColor("F")
                    if (QColorsMap.autoColor[5] != currentColor[5]):
                        QColorsMap.autoColor = currentColor
                        QColorsMap.newColorAdd()
                        QColorsMap.load()

        except:
            pass


    # ---- Various --------------------------------------------------------------------------------

    # Show/hide the start instructions.
    def showStartInstructions(show):
        if (show):
            QColorsMap.colorsMap.setText("Open a Krita document!\n(You can click here)")
            QColorsMap.colorsMap.setAlignment(Qt.AlignCenter)
        else:
            QColorsMap.colorsMap.setText("")

    # Show/hide map istructions.
    def showMapInstructions(show):
        if (show):
            QColorsMap.colorsMap.setText("Click here (or the [OPEN MAP] button below)\nto open an existing Colors Map\nor to create a new one.")
            QColorsMap.colorsMap.setAlignment(Qt.AlignCenter)
        else:
            QColorsMap.colorsMap.setText("")

    # Return True if a Colors Map has been loaded.
    def mapExists():
        return QColorsMap.fileName != ""

    # Return True if there isn't a Colors Map yet.
    def hasNoMap():
        return QColorsMap.fileName == ""

    # Check the validity of the fileName and return a valid fileName. Return "" if it's not valid.
    def checkFileName(fileName):
        if (fileName == ""): return ""
        if (FILE.exists(fileName)):
            if (not(FILE.checkExtension(fileName, ".cmap"))): fileName = ""
        else:
            if (fileName.find(".cmap") < 0): fileName += ".cmap"
        
        if (fileName == ""): ALERT.error("FILE NOT VALID", "The selected file is not valid.\n\nSelect a valid Colors Map file (.cmap file).")

        return fileName

    # Get the Color of the given index from the Colors Map file and return a Krita managed Color. Also, write the Color Label with the Color description.
    def createColorFromMap(index):
        fileContent = FILE.open(QColorsMap.fileName)
        tmp = fileContent[index].split("|")
        item = {
                "colorModel": tmp[4],
                "colorDepth": tmp[5],
                "colorProfile": tmp[6],
                "color01": float(tmp[7]),
                "color02": float(tmp[8]),
                "color03": float(tmp[9]),
                "color04": float(tmp[10]),
                "color05": float(tmp[11])
            }
        
        color = tmp[12]
        dist = "    "
        if (color.find("Red") >= 0): 
            color = color.replace("Red", "R").replace("Green", dist + "G").replace("Blue", dist + "B").replace("Alpha", dist + "A")
        elif (color.find("Yellow") >= 0): 
            color = color.replace("Cyan", "C").replace("Magenta", dist + "M").replace("Yellow", dist + "Y").replace("Black", dist + "K").replace("Alpha", dist + "A")
        elif (color.find("Lightness") >= 0): 
            color = color.replace("Lightness", "L").replace("a*", dist + "a*").replace("b*", dist + "b*").replace("Alpha", dist + "A")
        elif (color.find("Z") >= 0):
            color = color.replace("Y", dist + "Y").replace("Z", dist + "Z").replace("Alpha", dist + "A")
        elif (color.find("Cb") >= 0):
            color = color.replace("Cb", dist + "Cb").replace("Cr", dist + "Cr").replace("b*", dist + "b*").replace("Alpha", dist + "A")
        elif (color.find("Gray") >= 0):
            color = color.replace("Alpha", dist + "A")

        QColorsMap.colorLabel.setText(color)

        qColor = KRITA.createColor("KRITA", item["colorModel"], item["colorDepth"], item["colorProfile"], item["color01"], item["color02"], item["color03"], item["color04"], item["color05"])
        return qColor

    # Reset a Colors Map (usually, when a Krita document has been closed).
    def reset():
        QColorsMap.fileName = ""
        QColorsMap.map = list()

        pixmap = QPixmap(1, 1)
        pixmap.fill(Qt.transparent)
        QColorsMap.colorsMap.setPixmap(pixmap)
        QColorsMap.tempMap.setPixmap(pixmap)

        QColorsMap.colorLabel.setText("...")

    # Execute a check confronting the current Document Color Profile with the loaded Colors Map file profile.
    def colorsProfileCheck():
        currentProfile = KRITA.colorConfig()
        fileContent = FILE.open(QColorsMap.fileName)

        mismatch = False
        mismatchLine = ""
        for index, line in enumerate(fileContent):
            if (line.find(currentProfile["model"]) < 0 or line.find(currentProfile["depth"]) < 0):
                mismatch = True
                mismatchLine = line.split("|")

        if (mismatch):
            ALERT.info(
                "COLORS PROFILE MISMATCH", 
                "Your Krita's Document has " + currentProfile["model"] + " (" + currentProfile["depth"] + ") color profile.\n\n" +
                "Your Colors Map contains one or more colors with different profiles (found a color with " + mismatchLine[4] + " (" + mismatchLine[5] + ") profile).\n\n" +
                "Keep in mind that, even if this plugin can manage Colors with different profiles, in this case you may encounter some variation in your Colors."
                )

        


    # ---- Temporary Map click --------------------------------------------------------------------
    
    def onTempMapClick(event):
        if (KRITA.isNotReady()): return

        click = KRITA.getEvent(event)

        # RIGHT CLICK: just add a color at the end.
        if (click["right"]):
            if (click["noModifier"]):
                QColorsMap.newTempAdd()

        # LEFT CLICK: set Foreground, +SHIFT set Background.
        if (click["left"]):
            foundItem = QColorsMap.findTempIndex(click["x"], click["y"])
            if (foundItem["index"] < 0): return
            
            if (click["noModifier"]):
                KRITA.setColor("F", QColorsMap.createTempColor(foundItem["index"]))
            elif (click["isShift"]):
                KRITA.setColor("B", QColorsMap.createTempColor(foundItem["index"]))

    # Temporary Colors are added to the tempColorsMap List.
    def newTempAdd():
        newColor = KRITA.getSelectedColor("F")
        data = "[C]|[O]|[V]|" + "TEMPORARY_COLOR" + "|" + KRITA.colorParam("MODEL") + "|" + KRITA.colorParam("DEPTH") + "|" + KRITA.colorParam("PROFILE") + "|"
        for value in newColor: data += value + "|"

        QColorsMap.tempColorsMap.insert(0, data)
        pixmap = ColorsMapRender.renderTempColors(QColorsMap.tempColorsMap, QColorsMap.scrollTempArea)
        QColorsMap.tempMap.setPixmap(pixmap)

    # Return the index of the clicked Temporary color.
    def findTempIndex(x, y):
        index = math.floor(x / 18)
        l = len(QColorsMap.tempColorsMap)
        return { "index" : -1 } if (index < 0 or index >= l) else { "index": index }

    # Create a Color from the clicked Temporary color (its index).
    def createTempColor(index):
        tmp = QColorsMap.tempColorsMap[index].split("|")
        item = {
                "colorModel": tmp[4],
                "colorDepth": tmp[5],
                "colorProfile": tmp[6],
                "color01": float(tmp[7]),
                "color02": float(tmp[8]),
                "color03": float(tmp[9]),
                "color04": float(tmp[10]),
                "color05": float(tmp[11])
            }
        qColor = KRITA.createColor("KRITA", item["colorModel"], item["colorDepth"], item["colorProfile"], item["color01"], item["color02"], item["color03"], item["color04"], item["color05"])
        return qColor

