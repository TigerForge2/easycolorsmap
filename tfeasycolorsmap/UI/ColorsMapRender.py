from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *
import math

from .Tools import *
#from ..Core.ALERT import *
from ..Core.FILE import *
from ..Core.KRITA import *

# **** Colors Maps rendering engine ***************************************************************

class ColorsMapRender:
    def __init__(self):
        super().__init__()

    # Render the given Colors Map file and return a Dictionary with the rendered Pixmap and other info.
    def run(fileName, scrollArea, isPopUp = False):
        map = list()
        data = ColorsMapRender.readColorsMapFile(fileName)

        W = scrollArea.width() - data["scrollSize"]
        H = scrollArea.height() - data["scrollSize"]

        counters = ColorsMapRender.counters(W, data)
        cols = counters["cols"]
        rows = counters["rows"]
        colors = counters["colors"]
        titles = counters["titles"]

        counter = 0
        x = 0
        y = 0
        areaW = cols * data["colorSize"]
        areaH = (titles * data["titleSize"]) + (rows * data["colorSize"])

        pixmap = QPixmap(W, areaH)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        wasCollapsed = False
        isVisible = True

        for index, item in enumerate(data["items"]):
            if (item["isColor"] and not wasCollapsed and isVisible):

                painter = ColorsMapRender.drawColor(painter, item, x, y, data["colorSize"], data["colorFontSize"])
                map.append(str(index) + "|C|" + str(x) + "|" + str(y) + "|" + str(data["colorSize"]) + "|" + str(data["colorSize"]))

                counter += 1

                if (counter < cols):                    
                    x += data["colorSize"]
                else:
                    counter = 0
                    x = 0
                    y += data["colorSize"]

            elif (item["isGroup"] and item["isVisible"]):

                if (index > 0):
                    x = 0
                    y += data["colorSize"]
                    if (counter == 0): y -= data["colorSize"]

                ColorsMapRender.drawTitle(painter, item, data["titleSize"], data["titleFontSize"], x, y, W, isPopUp)
                map.append(str(index) + "|G|" + str(x) + "|" + str(y) + "|" + str(W) + "|" + str(data["titleSize"]))
                counter = 0
                x = 0
                y += data["titleSize"]
                wasCollapsed = not(item["isOpen"])
                isVisible = True

            elif (item["isGroup"] and not item["isVisible"]):
                isVisible = False

        painter.end()

        d = dict()
        d["pixmap"] = pixmap
        d["map"] = map
        d["cols"] = cols
        d["rows"] = rows
        d["titles"] = titles
        return d

    # Draw a colored box with an inner title.
    def drawColor(painter, item, x, y, colorSize, fontSize):

        # Requested data to show
        colorName = item["name"]
        qColor = KRITA.createColor("QCOLOR", item["colorModel"], item["colorDepth"], item["colorProfile"], item["color01"], item["color02"], item["color03"], item["color04"], item["color05"])
        useBlack = ColorsMapRender.getTextLuminance(qColor) > 0.5

        # Render
        Tools.drawRect(painter, Qt.black, qColor, x, y, colorSize, colorSize)
        Tools.drawBoxedText(painter, colorName, Qt.black if useBlack else Qt.white, fontSize, x, y, colorSize - 4, colorSize - 4)

        return painter
    
    # Get the luminance for the name of the Color. It uses the RGB model params of the given QColor.
    def getTextLuminance(qColor):
        return qColor.redF() * 0.299 + qColor.greenF() * 0.587 + qColor.blueF() * 0.114

    # Draw the Group collapsible title.
    def drawTitle(painter, item, titleSize, titleFontSize, x, y, w, isPopUp):
        
        # The collapsible rectangle container.
        Tools.drawRect(painter, Qt.black, Qt.black, x, y, w, titleSize)
        Tools.drawText(painter, item["name"], Qt.white, titleFontSize, x + 8, y + 18)

        if (not isPopUp):
            # The collapse icon [+] or [-]
            expX = w - titleSize + 2
            expY = y + 4
            expS = titleSize - 4 - 4
            Tools.drawRect(painter, Qt.gray, QColor(83, 114, 142), expX, expY, expS, expS)

            expIcon = ""
            offset = 3
            if (item["isOpen"]):
                expIcon = "-"
                offset = 5
            else:    
                expIcon = "+"

            Tools.drawText(painter, expIcon, Qt.white, titleFontSize, expX + offset, expY + 13)

    # Read the .cmap file and return an organizes structure of its content, suitable for the rendering process.
    def readColorsMapFile(fileName):
        fileContent = FILE.open(fileName)

        data = {
            "colorModel": "",
            "colorDepth": "",
            "colorProfile": "",
            "colorSize": 0,
            "titleSize": 0,
            "colorFontSize": 0,
            "titleFontSize": 0,
            "scrollSize": 0,
            "items": list()
        }

        for index, line in enumerate(fileContent):

            if (index == 0):
                # Colors Map configuration
                tmp = line.split("|")
                data["colorModel"] = tmp[3]
                data["colorDepth"] = tmp[4]
                data["colorProfile"] = tmp[5]
                data["colorSize"] = int(tmp[6])
                data["titleSize"] = int(tmp[7])
                data["colorFontSize"] = int(tmp[8])
                data["titleFontSize"] = int(tmp[9])
                data["scrollSize"] = int(tmp[10])
            else:
                # Groups and Colors
                tmp = line.split("|")
                if (tmp[0] == "[G]"):
                    data["items"].append({
                        "isGroup": True,
                        "isColor": False,
                        "isOpen": (tmp[1] == "[O]"),
                        "isVisible": (tmp[2] == "[V]"),
                        "name": tmp[3],
                        "colorModel": "",
                        "colorDepth": "",
                        "colorProfile": "",
                        "color01": 0,
                        "color02": 0,
                        "color03": 0,
                        "color04": 0,
                        "color05": 0,
                        "color": ""
                    })

                elif (tmp[0] == "[C]"):
                    data["items"].append({
                        "isGroup": False,
                        "isColor": True,
                        "isOpen": (tmp[1] == "[O]"),
                        "isVisible": (tmp[2] == "[V]"),
                        "name": tmp[3],
                        "colorModel": tmp[4],
                        "colorDepth": tmp[5],
                        "colorProfile": tmp[6],
                        "color01": float(tmp[7]),
                        "color02": float(tmp[8]),
                        "color03": float(tmp[9]),
                        "color04": float(tmp[10]),
                        "color05": float(tmp[11]),
                        "color": tmp[12]
                    })

        return data

    # Count and estimate the number of Rows, Columns, Colors and Groups
    def counters(W, data):
        cols = math.floor(W / data["colorSize"])
        rows = 0
        colors = 0
        titles = 0

        for index, item in enumerate(data["items"]):
            if (item["isColor"]):

                colors += 1

            elif (item["isGroup"]):

                titles += 1
                if (colors > 0):
                    rows += math.ceil(colors / cols)
                    colors = 0

        if (rows == 0):
            rows = math.ceil(colors / cols)
        elif (colors > 0):
            rows += math.ceil(colors / cols)

        return { "rows" : rows, "cols": cols, "colors": colors, "titles": titles }

    def renderTempColors(colorsMap, scrollArea):
        size = 16

        W = scrollArea.width()
        H = scrollArea.height()

        pixmap = QPixmap(W, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)

        x = 0
        y = 0

        colorsList = ColorsMapRender.readTempMap(colorsMap)

        for index, item in enumerate(colorsList["items"]):
            painter = ColorsMapRender.drawColor(painter, item, x, y, size, 4)
            x += size

        painter.end()
        return pixmap
        
    def readTempMap(colorsMap):

        data = {
            "colorModel": "",
            "colorDepth": "",
            "colorProfile": "",
            "colorSize": 0,
            "titleSize": 0,
            "colorFontSize": 0,
            "titleFontSize": 0,
            "scrollSize": 0,
            "items": list()
        }

        for index, line in enumerate(colorsMap):
            
            tmp = line.split("|")
            data["items"].append({
                        "isGroup": False,
                        "isColor": True,
                        "isOpen": True,
                        "isVisible": True,
                        "name": "",
                        "colorModel": tmp[4],
                        "colorDepth": tmp[5],
                        "colorProfile": tmp[6],
                        "color01": float(tmp[7]),
                        "color02": float(tmp[8]),
                        "color03": float(tmp[9]),
                        "color04": float(tmp[10]),
                        "color05": float(tmp[11]),
                        "color": tmp[12]
                        })

        return data