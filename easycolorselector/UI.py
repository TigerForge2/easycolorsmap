from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
from krita import *
from .ALERT import *
from .FILE import *
import math


class UI:
    def __init__(self):
        super().__init__()

    def toolBt(icon, f, toolTip = "", style = Qt.ToolButtonIconOnly, text = ""):
        bt = QToolButton()
        bt.setToolButtonStyle(style)
        bt.setIcon(Krita.instance().icon(icon))
        if (toolTip != ""): bt.setToolTip(toolTip)
        if (text != ""): bt.setText(text)
        bt.clicked.connect(f)
        return bt
        pass

    def bt(text, f, toolTip=""):
        bt = QPushButton()
        if (toolTip != ""):
            bt.setToolTip(toolTip)
        bt.setText(text)
        bt.clicked.connect(f)
        return bt
        pass

    def getFileSize(fileName):
        info = QFileInfo(fileName)
        return info.size()
        pass

    def getIcon(icon):
        return Krita.instance().icon(icon)

    def getCursor(icon):
        qIcon = Krita.instance().icon(icon)
        qIconPixmap = qIcon.pixmap(16, 16)
        return QCursor(qIconPixmap)

    def getForeground():
        activeView = Krita.instance().activeWindow().activeView()
        fColor = activeView.foregroundColor().components()
        d = dict()
        d["B"] = fColor[0]
        d["G"] = fColor[1]
        d["R"] = fColor[2]
        d["A"] = fColor[3]
        return d

    def getForegroundQColor():
        try:
            activeView = Krita.instance().activeWindow().activeView()
            fColor = activeView.foregroundColor().components()
            qColor = QColor()
            qColor.setBlueF(fColor[0])
            qColor.setGreenF(fColor[1])
            qColor.setRedF(fColor[2])
            qColor.setAlphaF(fColor[3])
            return qColor
        except:
            return None

    def renderColorsMap(fileName, areaSize):
        map = list()
        fileContent = FILE.open(fileName)
        W = areaSize.width() - 16
        H = areaSize.height() - 16

        cols = math.floor(W / 42)
        rows = 0
        colors = 0
        titles = 0
        for index, line in enumerate(fileContent):
            if (UI.lineIsColor(line)):

                colors += 1

            elif (UI.lineIsTitle(line)):

                titles += 1
                if (colors > 0):
                    rows += math.ceil(colors / cols)
                    colors = 0

        if (rows == 0):
            rows = math.ceil(colors / cols)
        elif (colors > 0):
            rows += math.ceil(colors / cols)

        counter = 0
        x = 0
        y = 0
        areaW = cols * 42
        areaH = (titles * 24) + (rows * 42)

        pixmap = QPixmap(areaW, areaH)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)

        for index, line in enumerate(fileContent):
            if (UI.lineIsColor(line)):

                data = line.split("|")
                painter = UI.drawColor(painter, data, x, y)
                map.append(str(index) + "|C|" + str(x) + "|" + str(y) + "|42|42")

                counter += 1

                if (counter < cols):                    
                    x += 42
                else:
                    counter = 0
                    x = 0
                    y += 42

            elif (UI.lineIsTitle(line)):

                if (index > 0):
                    x = 0
                    y += 42
                    if (counter == 0): y -= 42

                UI.drawTitle(painter, line, x, y, areaW)
                map.append(str(index) + "|T|" + str(x) + "|" + str(y) + "|" + str(areaW) + "|24")
                counter = 0
                x = 0
                y += 24

        painter.end()

        d = dict()
        d["pixmap"] = pixmap
        d["map"] = map
        return d
        pass

    def drawColor(painter, data, x, y, size = 42):

        colorName = data[0]
        colorB = float(data[1])
        colorG = float(data[2])
        colorR = float(data[3])
        colorA = float(data[4])

        luminance = colorR * 0.299 + colorG * 0.587 + colorB * 0.114
        useBlack = luminance > 0.5

        qColor = QColor()
        qColor.setBlueF(colorB)
        qColor.setGreenF(colorG)
        qColor.setRedF(colorR)
        qColor.setAlphaF(colorA)

        painter.setBrush(QBrush(qColor, Qt.SolidPattern))
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawRect(x, y, size, size)

        if (colorName == "RGB"):
            colorName = str(qColor.red()) + "  " + \
                str(qColor.green()) + "  " + str(qColor.blue())

        font = painter.font()
        font.setPixelSize(10)
        painter.setFont(font)

        if (useBlack > 0.150):
            painter.setPen(QPen(Qt.black, 1))
        else:
            painter.setPen(QPen(Qt.white, 1))

        rectangle = QRect(x + 2, y, 42 - 4, 42 - 4)
        boundingRect = QRect()
        painter.drawText(rectangle, Qt.TextWordWrap, colorName)

        return painter
        pass

    def drawTitle(painter, data, x, y, w):
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawRect(x, y, w, 24)

        font = painter.font()
        font.setPixelSize(16)
        painter.setFont(font)
        painter.setPen(QPen(Qt.white, 1))
        painter.drawText(x + 8, y + 18, data)

        return painter
        pass

    def lineIsColor(line):
        if (line == ""): return False
        return (line.find("#") != 0 and line.find("|") > 0)

    def lineIsTitle(line):
        if (line == ""): return False
        return (line.find("#") < 0 and line.find("|") < 0)

    def renderTempMap(map, areaSize):
        size = 16
        W = areaSize.width() - 2
        H = areaSize.height()

        pixmap = QPixmap(W, size)
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)

        x = 0
        y = 0

        for index, color in enumerate(map):
            painter.setBrush(QBrush(color, Qt.SolidPattern))
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            painter.drawRect(x, y, size, size)
            x += size

        painter.end()
        return pixmap
        pass
