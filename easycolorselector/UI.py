from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from krita import *
from .SYS import *
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

    def contextMenu(self):
        contextMenu = QMenu(self)
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
        return menuItems


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
            if (UI.isRGB()):
                return QColor.fromRgbF(fColor[2], fColor[1], fColor[0], fColor[3])
            else:
                return QColor.fromCmykF(fColor[0], fColor[1], fColor[2], fColor[3], fColor[4])
        except:
            return None

    def getBackgroundQColor():
        try:
            activeView = Krita.instance().activeWindow().activeView()
            fColor = activeView.backgroundColor().components()
            if (UI.isRGB()):
                return QColor.fromRgbF(fColor[2], fColor[1], fColor[0], fColor[3])
            else:
                return QColor.fromCmykF(fColor[0], fColor[1], fColor[2], fColor[3], fColor[4])
        except:
            return None

    def getColorParams(color):
        if (UI.isRGB()):
            return str(color.blueF()) + "|" + str(color.greenF()) + "|" + str(color.redF()) + "|" + str(color.alphaF())
        else:
            return str(color.cyanF()) + "|" + str(color.magentaF()) + "|" + str(color.yellowF()) + "|" + str(color.blackF()) + "|" + str(color.alphaF())

    def setAnnotation(fileName):
        activeView = Krita.instance().activeDocument()
        activeView.setAnnotation('TFECMAP', "Path to TF Easy Colors Map", QByteArray(fileName.encode()))
        pass

    def getAnnotation():
        try:
            activeView = Krita.instance().activeDocument()
            annotation = activeView.annotation('TFECMAP')
            if (annotation is None):
                return ""
            else:
                return bytes(annotation).decode()
        except:
            return ""
        pass

    def setForeGroundColor(color):
        activeView = Krita.instance().activeWindow().activeView()
        activeView.setForeGroundColor(color) 

    def setBackGroundColor(color):
        activeView = Krita.instance().activeWindow().activeView()
        activeView.setBackGroundColor(color) 

    def colorProfile():
        activeView = Krita.instance().activeDocument()
        if (activeView.colorModel() == "RGBA"):
            return "RGB"
        else:
            return "CMYK"

    def isRGB():
        return UI.colorProfile() == "RGB"

    def isCMYK():
        return UI.colorProfile() == "CMYK"

    def colorDepth():
        activeView = Krita.instance().activeDocument()
        return activeView.colorDepth()

    def noKritaDoc():
        return Krita.instance().activeDocument() is None

    def getColorFromIndex(fileName, index):
        fileContent = FILE.open(fileName)
        return fileContent[index]

    def getManagedColor(a, b, c, d):
        if (UI.colorProfile() == "RGB"):
            myColor = ManagedColor("RGBA", UI.colorDepth(), "")
            colorComponents = myColor.components()
            colorComponents[0] = a
            colorComponents[1] = b
            colorComponents[2] = c
            colorComponents[3] = 1
        else:
            myColor = ManagedColor("CMYKA", UI.colorDepth(), "")
            colorComponents = myColor.components()
            colorComponents[0] = a
            colorComponents[1] = b
            colorComponents[2] = c
            colorComponents[3] = d
            colorComponents[4] = 1
        
        myColor.setComponents(colorComponents)
        return(myColor)

    def getManagedColorFromQColor(qColor):
        if (UI.colorProfile() == "RGB"):
            myColor = ManagedColor("RGBA", UI.colorDepth(), "")
            colorComponents = myColor.components()
            colorComponents[0] = qColor.blueF()
            colorComponents[1] = qColor.greenF()
            colorComponents[2] = qColor.redF()
            colorComponents[3] = 1
        else:
            myColor = ManagedColor("CMYKA", UI.colorDepth(), "")
            colorComponents = myColor.components()
            colorComponents[0] = qColor.cyanF()
            colorComponents[1] = qColor.magentaF()
            colorComponents[2] = qColor.yellowF()
            colorComponents[3] = qColor.blackF()
            colorComponents[4] = 1
        
        myColor.setComponents(colorComponents)
        return(myColor)

    def createCMYK(c, m, y, k):
        myColor = ManagedColor("CMYKA", UI.colorDepth(), "")
        colorComponents = myColor.components()
        colorComponents[0] = c
        colorComponents[1] = m
        colorComponents[2] = y
        colorComponents[3] = k
        colorComponents[4] = 1
        myColor.setComponents(colorComponents)
        canvas = Krita.instance().activeWindow().activeView().canvas()
        return(myColor.colorForCanvas(canvas))

    def createRGB(r, g, b):
        myColor = ManagedColor("RGBA", UI.colorDepth(), "")
        colorComponents = myColor.components()
        colorComponents[0] = b
        colorComponents[1] = g
        colorComponents[2] = r
        colorComponents[3] = 1
        myColor.setComponents(colorComponents)
        canvas = Krita.instance().activeWindow().activeView().canvas()
        return(myColor.colorForCanvas(canvas))

    def renderColorsMap(fileName, areaSize):
        map = list()
        fileContent = FILE.open(fileName)
        W = areaSize.width() - SYS.config["scrollSize"]
        H = areaSize.height() - SYS.config["scrollSize"]

        cols = math.floor(W / SYS.config["colorSize"])
        rows = 0
        colors = 0
        titles = 0
        for index, line in enumerate(fileContent):
            if (SYS.lineIsColor(line)):

                colors += 1

            elif (SYS.lineIsTitle(line)):

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
        areaW = cols * SYS.config["colorSize"]
        areaH = (titles * SYS.config["titleSize"]) + (rows * SYS.config["colorSize"])

        pixmap = QPixmap(areaW, areaH)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        wasCollapsed = False

        for index, line in enumerate(fileContent):
            if (SYS.lineIsColor(line) and not wasCollapsed):

                data = line.split("|")
                painter = UI.drawColor(painter, data, x, y)
                map.append(str(index) + "|C|" + str(x) + "|" + str(y) + "|" + str(SYS.config["colorSize"]) + "|" + str(SYS.config["colorSize"]))

                counter += 1

                if (counter < cols):                    
                    x += SYS.config["colorSize"]
                else:
                    counter = 0
                    x = 0
                    y += SYS.config["colorSize"]

            elif (SYS.lineIsTitle(line)):

                if (index > 0):
                    x = 0
                    y += SYS.config["colorSize"]
                    if (counter == 0): y -= SYS.config["colorSize"]

                UI.drawTitle(painter, line, x, y, areaW)
                map.append(str(index) + "|T|" + str(x) + "|" + str(y) + "|" + str(areaW) + "|" + str(SYS.config["titleSize"]))
                counter = 0
                x = 0
                y += SYS.config["titleSize"]
                wasCollapsed = (line.find(">") == 0)

        painter.end()

        d = dict()
        d["pixmap"] = pixmap
        d["map"] = map
        d["cols"] = cols
        d["rows"] = rows
        d["titles"] = titles
        return d
        pass

    def drawColor(painter, data, x, y):

        colorName = data[0]

        qColor = UI.createColorFromParams(data)

        luminance = UI.getLuminance(data)
        useBlack = luminance > 0.5
        if (UI.isCMYK()): useBlack = luminance < 0.5

        painter.setBrush(QBrush(qColor, Qt.SolidPattern))
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawRect(x, y, SYS.config["colorSize"], SYS.config["colorSize"])

        font = painter.font()
        font.setPixelSize(SYS.config["colorFontSize"])
        painter.setFont(font)

        if (useBlack > 0.150):
            painter.setPen(QPen(Qt.black, 1))
        else:
            painter.setPen(QPen(Qt.white, 1))

        rectangle = QRect(x + 2, y, SYS.config["colorSize"] - 4, SYS.config["colorSize"] - 4)
        boundingRect = QRect()
        painter.drawText(rectangle, Qt.TextWordWrap, colorName)

        return painter
        pass

    def createColorFromParams(data):
        qColor = QColor()
        if (UI.isRGB()):
            qColor = UI.createRGB(float(data[3]), float(data[2]), float(data[1]))
        else:
            qColor = UI.createCMYK(float(data[1]), float(data[2]), float(data[3]), float(data[4]))

        return qColor

    def createColorFromQColor(qColor):
        color = QColor()
        if (UI.isRGB()):
            color = UI.createRGB(qColor.redF(), qColor.greenF(), qColor.blueF())
        else:
            color = UI.createCMYK(qColor.cyanF(), qColor.magentaF(), qColor.yellowF(), qColor.blackF())

        return color
    
    def getLuminance(data):
        if (UI.isRGB()):
            return float(data[3]) * 0.299 + float(data[2]) * 0.587 + float(data[1]) * 0.114
        else:
            return float(data[1]) * 0.299 + float(data[2]) * 0.587 + float(data[3]) * 0.114

    def drawTitle(painter, data, x, y, w):
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawRect(x, y, w, SYS.config["titleSize"])

        expX = w - SYS.config["titleSize"] + 2
        expY = y + 4
        expS = SYS.config["titleSize"] - 4 - 4
        painter.setPen(QPen(Qt.gray, 1))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawRect(expX, expY, expS, expS)

        expIcon = ""
        offset = 3
        if (data.find(">") == 0):
            data = data[1:]
            expIcon = "+"
        else:    
            expIcon = "-"
            offset = 5

        font = painter.font()
        font.setPixelSize(SYS.config["titleFontSize"])
        painter.setFont(font)
        painter.setPen(QPen(Qt.white, 1))
        painter.drawText(x + 8, y + 18, data)
        painter.drawText(expX + offset, expY + 13, expIcon)

        return painter
        pass

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
            myColor = UI.createColorFromQColor(color)
            painter.setBrush(QBrush(myColor, Qt.SolidPattern))
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            painter.drawRect(x, y, size, size)
            x += size

        painter.end()
        return pixmap
        pass

    def find_current_canvas():
        try:
            app = Krita.instance()
            q_window = app.activeWindow().qwindow()
            q_stacked_widget = q_window.centralWidget()
            q_mdi_area = q_stacked_widget.currentWidget()
            q_mdi_sub_window = q_mdi_area.currentSubWindow()
            view = q_mdi_sub_window.widget()
            for c in view.children():
                if c.metaObject().className() == 'KisCanvasController':
                    viewport = c.viewport()
                    canvas = viewport.findChild(QWidget)
                    return canvas
            return None
        except:
            return None

    def get_my_canvas(myCanvas = None):
        if (myCanvas is None):
            canvas = UI.find_current_canvas()
        else:
            canvas = myCanvas

        if (not canvas is None):
            global_pos = QCursor.pos()
            pos = QPoint(canvas.mapFromGlobal(global_pos))
            if (pos.x() < 0 or pos.y() < 0 or pos.x() > canvas.width() or pos.y() > canvas.height()):
                return { "canvas": canvas, "x": 0, "y": 0, "isInside": False, "globalPos": global_pos }
            else:
                return { "canvas": canvas, "x": pos.x(), "y": pos.y(), "isInside": True, "globalPos": global_pos }
        return { "canvas": None, "x": 0, "y": 0, "isInside": False, "globalPos": None }

    def dump_tree(self,qobj):
        #qwindow = Krita.instance().activeWindow().qwindow()
        #self.dump_tree(qwindow)
        stack = [(qobj, 0)]
        while stack:
            cursor, depth = stack.pop(-1)  # depth first
            indent = depth * "  "
            cls_name = type(cursor).__name__
            meta_cls_name = cursor.metaObject().className()
            obj_name = cursor.objectName()
            ALERT.log(f"{indent}cls: {cls_name}, meta_cls_name: {meta_cls_name}, obj_name: {obj_name!r}")
            stack.extend((c, depth +1) for c in cursor.children())
    
    def kritaDrawingToolSelected():
        tools = [
            "KritaShape/KisToolMultiBrush",
            "KritaShape/KisToolLine",
            "KritaShape/KisToolBrush",
            "KisToolPolyline",
            "KritaShape/KisToolRectangle",
            "KritaShape/KisToolDyna",
            "KisToolPath",
            "KritaShape/KisToolEllipse",
            "KisToolPolygon",
            "KisToolPencil",
            "KritaFill/KisToolFill",
            "KritaFill/KisToolGradient",
            "KritaShape/KisToolLazyBrush"
            ]
        qwindow = Krita.instance().activeWindow().qwindow()

        for item in tools:
            target_qobj = qwindow.findChild(QToolButton, item)
            if (target_qobj.isChecked()): return True

        return False

    def getGroupsList(fileName):
        fileContent = FILE.open(fileName)
        groups = list()
        for index, line in enumerate(fileContent):
            if (SYS.lineIsTitle(line)):
                if (line.find(">") == 0): line = line[1:]
                groups.append(line)
        
        return groups

    def createQWidgetLayout(direction, alignment):
        formLayout = QWidget()
        fL = QVBoxLayout()
        if (direction == "H"): fL = QHBoxLayout()
        fL.setAlignment(alignment)
        formLayout.setLayout(fL)
        return formLayout
        
