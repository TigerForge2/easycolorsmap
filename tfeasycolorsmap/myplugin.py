from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer

from krita import *

from .Core.SYS import *
from .Core.KRITA import *
from .Core.ALERT import *
from .UI.UI import *

# **** TF Easy Colors Map - Krita Plugin **********************************************************

class TFEasyColorsMapDocker(DockWidget):

    def __init__(self):
        super().__init__()

        # Plugin version.
        SYS.version = 21

        # The plugin UI is managed by the UI class.
        UI.body = self
        UI.render()
        

    def canvasChanged(self, canvas):
        # Mandatory class: must be declared.
        pass

    # Define an Event Filter for this plugin when Right Click + SHIFT is permormed on the Krita Document Canvas.
    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton and event.modifiers() == Qt.ShiftModifier:

                if (KRITA.drawingToolSelected()):
                    c = KRITA.getCurrentCanvas()
                    pos = c["globalPos"]
                    UI.showColorsPopUp(pos.x(), pos.y())

        return super().eventFilter(object, event)

Krita.instance().addDockWidgetFactory(DockWidgetFactory(
    "TF_Easy_Colors_Map", DockWidgetFactoryBase.DockRight, TFEasyColorsMapDocker))


