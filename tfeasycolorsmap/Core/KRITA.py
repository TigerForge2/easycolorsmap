from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from .ALERT import *

# **** Krita components access helpers ************************************************************

class KRITA:
    def __init__(self):
        super().__init__()

    def App():
        """The Krita instance: Krita.instance()"""
        return Krita.instance()

    def Document():
        """The Krita active Document: Krita.instance().activeDocument()"""
        return Krita.instance().activeDocument()

    def AppNotifier():
        """Return a Krita active Notifier."""
        appNotifier = Krita.instance().notifier()
        appNotifier.setActive(True)
        return appNotifier

    def View():
        """The Krita active View: Krita.instance().activeWindow().activeView()"""
        return Krita.instance().activeWindow().activeView()

    def Window():
        """The Krita active Window: Krita.instance().activeWindow()"""
        return Krita.instance().activeWindow()

    def getSelectedColor(target):
        """Get the View selected color from the given target (F: foreground, B: background) as an array of 6 string. Where the color is not available a -1 value is placed. The last value (index = 5) is the color description."""
        view = KRITA.View()
        color = view.foregroundColor() if target == "F" else view.backgroundColor()
        config = KRITA.colorConfig()
        color.setColorSpace(config["model"], config["depth"], config["profile"])

        selectedColor = ["-1", "-1", "-1", "-1", "-1", ""]

        colorData = color.components()
        for index, value in enumerate(colorData): selectedColor[index] = str(value)
        selectedColor[5] = color.toQString()

        return selectedColor

    def setColor(target, color):
        """Set the Krita (F: foreground, B: background) color with the given Krita managed Color."""
        view = KRITA.View()
        if (target == "F"): 
            view.setForeGroundColor(color) 
        else: 
            view.setBackGroundColor(color) 

    def getEvent(event):
        """Extract informations from a Krita event and return an organized Dictionary."""
        modifierPressed = QApplication.keyboardModifiers()
        isShift = (modifierPressed & Qt.ShiftModifier)
        isCtrl = (modifierPressed & Qt.ControlModifier)
        isAlt = (modifierPressed & Qt.AltModifier)
        leftClick = (event.buttons() == Qt.LeftButton)
        rightClick = (event.buttons() == Qt.RightButton)
        x = event.pos().x()
        y = event.pos().y()
        globalPos = event.globalPos()

        return {
            "hasModifier" : modifierPressed,
            "noModifier" : not(modifierPressed),
            "isShift" : isShift,
            "isCtrl" : isCtrl,
            "isAlt" : isAlt,
            "left" : leftClick,
            "right" : rightClick,
            "x" : x,
            "y" : y,
            "globalPos" : globalPos
        }

    def colorConfig():
        """Return a Dictionary containing the various current Document colors settings (depth, model, profile)."""
        doc = KRITA.Document()
        return {
            "depth": doc.colorDepth(),
            "model": doc.colorModel(),
            "profile": doc.colorProfile()
        }

    def colorParam(param):
        """Return the requested current Color MODEL / DEPTH / PROFILE."""
        doc = KRITA.Document()
        if (param == "MODEL"): return doc.colorModel()
        if (param == "DEPTH"): return doc.colorDepth()
        if (param == "PROFILE"): return doc.colorProfile()
        return ""

    def cursor(icon):
        """Get a Krita icon into a QCursor widget."""
        qIcon = KRITA.App().icon(icon)
        qIconPixmap = qIcon.pixmap(16, 16)
        return QCursor(qIconPixmap)

    def isNotReady():
        """Return True if Krita has no opened Documents."""
        return KRITA.Document() is None

    def isReady():
        """Return True if Krita has an opened Documents."""
        return not(KRITA.isNotReady())

    def createColor(returnAs, model, depth, profile, color01 = -1, color02 = -1, color03 = -1, color04 = -1, color05 = -1):
        """Build a Krita Managed Color with the given params. returnAs can be 'QCOLOR' if a QColor is needed or 'KRITA' if a ManagedColor component is needed."""
        myColor = ManagedColor(model, depth, profile)
        colorComponents = myColor.components()
        if (color01 >= 0): colorComponents[0] = color01
        if (color02 >= 0): colorComponents[1] = color02
        if (color03 >= 0): colorComponents[2] = color03
        if (color04 >= 0): colorComponents[3] = color04
        if (color05 >= 0): colorComponents[4] = color05
        myColor.setComponents(colorComponents)

        if (returnAs == "QCOLOR"):
            canvas = Krita.instance().activeWindow().activeView().canvas()
            return(myColor.colorForCanvas(canvas))
        else:
            return myColor

    def annotationSet(fileName):
        """Set the fileName as an internal annotation for the currently active Krita Document."""
        doc = KRITA.Document()
        doc.setAnnotation('TFECMAP2', "Path to TF Easy Colors Map V2", QByteArray(fileName.encode()))

    def annotationGet():
        """Return the fileName saved in the internal annotation of the currently active Krita Document."""
        try:
            doc = KRITA.Document()
            annotation = doc.annotation('TFECMAP2')
            if (annotation is None):
                return ""
            else:
                return bytes(annotation).decode()
        except:
            return ""

    def hasActiveViews():
        """Return TRUE if there are opened Documents in Krita."""
        win = KRITA.Window()
        return len(win.views()) > 1

    def actionTrigger(actionName):
        """Trigger a Krita action."""
        Krita.instance().action(actionName).trigger()

    def getCurrentCanvas(myCanvas = None):
        """Return a reference to the current or given Canvas with extra infos (x/y mouse coordinates, isInside and globalPos properties)."""
        if (myCanvas is None):
            canvas = KRITA.find_current_canvas()
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

    def drawingToolSelected():
        """Return True if the currently selected Krita Tool is a Drawing tool (Brush, Line, Pencil, Filler, etc.)."""
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