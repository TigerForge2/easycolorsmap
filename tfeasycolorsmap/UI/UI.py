from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from ..Core.SYS import *
from ..Core.KRITA import *
from ..Core.ALERT import *
from .QColorsMap import *
from .Tools import *
from ..Forms.FormsManager import *

# **** Plugin UI management ***********************************************************************

class UI:
    def __init__(self):
        super().__init__()

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, value):
        self.__body = value

    def render():
        UI.body.setWindowTitle("TF Easy Colors Map v." + SYS.getVersionString())
        mainWidget = QWidget(UI.body)
        UI.body.setWidget(mainWidget)

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainWidget.setLayout(mainLayout)

        # ---- MAPS

        # The Colors Maps are managed by the QColorsMap class.
        mainWidget.layout().addWidget(QColorsMap.render(mainWidget, UI.body))

        # ---- TOOLBAR

        bt_Open = Tools.toolBt('document-open', UI.toolbar_FileOpen, "OPEN MAP\nLoad an existing Colors Map or create a new one.")
        bt_Edit = Tools.toolBt('document-edit', UI.toolbar_Edit, "MAP EDITOR\nEdit the current Colors Map.")
        bt_Config = Tools.toolBt('config-performance', UI.toolbar_Config, "SETTINGS\nChange the settings of this Colors Map.")
        UI.bt_AutoColor = Tools.toolBt('fillLayer', UI.toolbar_AutoColor, "AUTO ADD COLORS\nStart/stop the Colors auto-acquisition system.")
        UI.bt_AutoColor.setCheckable(True)
        bt_Help = Tools.toolBt('document-open', UI.toolbar_Help, "GUIDE\nShow the inline guide.", Qt.ToolButtonTextOnly, "?")
            
        toolbar = Tools.QWidgetLayout("H")
        toolbar.layout().addWidget(bt_Open)
        toolbar.layout().addWidget(UI.bt_AutoColor)
        toolbar.layout().addWidget(bt_Edit)
        toolbar.layout().addWidget(bt_Config)
        toolbar.layout().addWidget(bt_Help)
        
        mainWidget.layout().addWidget(toolbar)

        # ---- Plugin behaviours on Krita application statuses

        an = KRITA.AppNotifier()
        an.viewCreated.connect(UI.notifier_View_Created)
        an.viewClosed.connect(UI.notifier_View_Closed)
        an.windowCreated.connect(UI.notifier_Window_Created)
        an.applicationClosing.connect(UI.notifier_App_Closing)

        # ---- FORMS initialization

        FORMS.initialize(UI.form_ConfigClose, UI.form_EditorClose)

    # ==== TOOLBAR ================================================================================

    def toolbar_FileOpen():
        QColorsMap.openFileDialog()

    def toolbar_Edit():
        if (KRITA.isNotReady() or QColorsMap.hasNoMap()):
            ALERT.warn("ATTENTION", "There is not a Colors Map yet.")
            return

        ALERT.info("COLORS MAP FILE EDITOR", "This Editor will open your Colors Map file and allows you to manually edit it.\n\nUse it with caution!\n\nA wrong modification may corrupt this file.")
        FORMS.show("EDITOR", QColorsMap.fileName)

    def toolbar_Config():
        if (KRITA.isNotReady() or QColorsMap.hasNoMap()):
            ALERT.warn("ATTENTION", "There is not a Colors Map yet.")
            return

        FORMS.show("CONFIG", QColorsMap.fileName)

    def toolbar_AutoColor():
        if (not QColorsMap.autoColor is None):
            QColorsMap.autoColor = None
            return

        if (KRITA.isNotReady() or QColorsMap.hasNoMap()):
            ALERT.warn("ATTENTION", "There is not a Colors Map yet.")
            return

        ALERT.info("AUTO-COLOR TOOL READY", "The Auto-Color acquisition tool is ready!\n\nNow, use the Krita Color Sampler tool for catching the Colors you want. For each Color, this plugin will ask you for a name.\n\nRemember to click this button again to stop Auto-Color!")
        QColorsMap.autoColor = KRITA.getSelectedColor("F")
        KRITA.actionTrigger("KritaSelected/KisToolColorSampler")

    def toolbar_Help():
        FORMS.show("HELP")

    # ==== NOTIFIERS ==============================================================================

    # When a new or an existing Document is opened (click on 'New File' or 'Open File').
    def notifier_View_Created():
        pass

    # When a document is closed (just a Document, not Krita).
    def notifier_View_Closed():
        QColorsMap.reset()
        pass

    # When Krita app has been opened, it's ready and accessible.
    def notifier_Window_Created():
        pass


    # When Krita is closing.
    def notifier_App_Closing():
        pass
    
    # ==== FORMS ==================================================================================

    def form_ConfigClose(self):
        QColorsMap.load()

    def form_EditorClose(self):
        QColorsMap.load()

    def showColorsPopUp(x, y):
        FORMS.show("COLORSPOPUP", QColorsMap.fileName, x, y)