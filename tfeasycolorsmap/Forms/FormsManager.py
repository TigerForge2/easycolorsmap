from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from .CONFIG import *
from .EDITOR import *
from .HELP import *
from .COLORSPOPUP import *

# **** FORMS management ***************************************************************************

class FORMS:
    def __init__(self):
        super().__init__()

    @property
    def ConfigForm(self):
        return self.__ConfigForm
    @ConfigForm.setter
    def ConfigForm(self, value):
        self.__ConfigForm = value

    @property
    def EditorForm(self):
        return self.__EditorForm
    @EditorForm.setter
    def EditorForm(self, value):
        self.__EditorForm = value

    @property
    def HelpForm(self):
        return self.__HelpForm
    @HelpForm.setter
    def HelpForm(self, value):
        self.__HelpForm = value

    @property
    def ColorsPopupForm(self):
        return self.__ColorsPopupForm
    @ColorsPopupForm.setter
    def ColorsPopupForm(self, value):
        self.__ColorsPopupForm = value

    def initialize(configClose, editorClose):

        FORMS.ConfigForm = CONFIG()
        FORMS.ConfigForm.closeEvent = configClose

        FORMS.EditorForm = EDITOR()
        FORMS.EditorForm.closeEvent = editorClose

        FORMS.HelpForm = HELP()

        FORMS.ColorsPopupForm = COLORSPOPUP()

    def show(formName, data = "", x = 0, y = 0):
        
        if (formName == "CONFIG"):
            FORMS.ConfigForm.init(data)
            FORMS.ConfigForm.show()

        if (formName == "EDITOR"):
            FORMS.EditorForm.read(data)
            FORMS.EditorForm.show()

        if (formName == "HELP"):
            FORMS.HelpForm.init()
            FORMS.HelpForm.show()

        if (formName == "COLORSPOPUP"):
            FORMS.ColorsPopupForm.read(data)
            FORMS.ColorsPopupForm.show()
            FORMS.ColorsPopupForm.move(x, y)
