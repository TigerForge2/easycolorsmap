from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

from krita import *
from ..Core.ALERT import *

# **** UI Helpers *********************************************************************************

class Tools:
    def __init__(self):
        super().__init__()

    # Create a TOOLBAR Button.
    def toolBt(icon, f, toolTip = "", style = Qt.ToolButtonIconOnly, text = ""):
        bt = QToolButton()
        bt.setToolButtonStyle(style)
        bt.setIcon(Krita.instance().icon(icon))
        if (toolTip != ""): bt.setToolTip(toolTip)
        if (text != ""): bt.setText(text)
        bt.clicked.connect(f)
        return bt
    
    # Create a simple PUSH Button.
    def bt(text, f, toolTip=""):
        bt = QPushButton()
        if (toolTip != ""):
            bt.setToolTip(toolTip)
        bt.setText(text)
        bt.clicked.connect(f)
        return bt

    # Create a QWidget with a Layout direction and alignment.
    def QWidgetLayout(direction, alignment = "", enableMargins = False):
        formLayout = QWidget()
        fL = QVBoxLayout()
        if (direction == "H"): fL = QHBoxLayout()
        if (alignment != ""): fL.setAlignment(alignment)
        if (enableMargins): fL.setContentsMargins(0, 10, 6, 0)
        formLayout.setLayout(fL)
        return formLayout

    # Return a configured QTimer interval Widget.
    def interval(f, time, start = False):
        timer = QTimer()
        timer.timeout.connect(f)
        timer.setInterval(time)
        if (start): timer.start()
        return timer

    # Return a configured QTimer timeout Widget.
    def timeout(f, time, start = True):
        timer = QTimer()
        timer.timeout.connect(f)
        timer.setInterval(time)
        timer.setSingleShot(True)
        if (start): timer.start()
        return timer

    # Draw a rectangle into the given 'painter'
    def drawRect(painter, penColor, brushColor, x, y, w, h, penSize = 1, brushPattern = Qt.SolidPattern):
        painter.setPen(QPen(penColor, penSize, Qt.SolidLine))
        painter.setBrush(QBrush(brushColor, brushPattern))
        painter.drawRect(x, y, w, h)
        return painter

    # Draw a text into the given 'painter'
    def drawText(painter, text, textColor, fontSize, x, y, style = ""):
        font = painter.font()
        font.setPixelSize(fontSize)
        font.setItalic(True if style == "i" else False)
        
        painter.setFont(font)
        painter.setPen(QPen(textColor, 1, Qt.SolidLine))
        painter.drawText(x, y, text)
        return painter

    # Draw a boxed text into the given 'painter'
    def drawBoxedText(painter, text, textColor, fontSize, x, y, width, height, style = ""):
        font = painter.font()
        font.setPixelSize(fontSize)
        font.setItalic(True if style == "i" else False)
        
        painter.setFont(font)
        painter.setPen(QPen(textColor, 1, Qt.SolidLine))
        rectangle = QRect(x + 2, y, width, height)
        painter.drawText(rectangle, Qt.TextWordWrap, text)
        return painter

    def contextMenu():
        contextMenu = QMenu()
        contextMenu.setToolTipsVisible(True)
        return contextMenu

    def contextMenuItems(cM, data):
        menuItems = dict()
        for item in data:
            if (item[0] == "-"):
                cM.addSeparator()
            else:
                menuItems[item[0]] = cM.addAction(item[1])
                menuItems[item[0]].setToolTip(item[2])
                menuItems[item[0]].setIconText(item[0])
        return menuItems

    def isProperty(value):
        string = str(value)
        return string.find("property") >= 0

    # Remove strings that may compromise the Colors Map.
    def sanitizeName(name):
        name = name.replace("|", "")
        name = name.replace("[C]", "")
        name = name.replace("[G]", "")
        name = name.replace("[O]", "")
        name = name.replace("[V]", "")
        name = name.replace("[X]", "")
        name = name.replace("[-]", "")
        name = name.replace("\n", "")
        return name