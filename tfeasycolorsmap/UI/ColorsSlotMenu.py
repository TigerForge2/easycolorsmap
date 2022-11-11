from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from .Tools import *
from ..Core.FILE import *
from ..Core.ALERT import *

# **** Colors Slots management *********************************************************************

class ColorsSlotMenu:

    @property
    def contextMenu(self):
        return self.__contextMenu

    @contextMenu.setter
    def contextMenu(self, value):
        self.__contextMenu = value

    @property
    def contextMenuItems(self):
        return self.__contextMenuItems

    @contextMenuItems.setter
    def contextMenuItems(self, value):
        self.__contextMenuItems = value

    @property
    def slot(self):
        return self.__slot

    @slot.setter
    def slot(self, value):
        self.__slot = value

    def __init__(self):
        super().__init__()

    def show(globalPos, itemIndex, fileName):
        ColorsSlotMenu.contextMenu = Tools.contextMenu()
        ColorsSlotMenu.contextMenuItems = Tools.contextMenuItems(
            ColorsSlotMenu.contextMenu,
            [
                ["[Slot_0]", "Main Slot", "Show the Colors of the Main Slot (shared Colors)."],
                ["-"],
                ["[Slot_1]", "Slot 1", "Show the Colors of the Slot 1."],
                ["[Slot_2]", "Slot 2", "Show the Colors of the Slot 2."],
                ["[Slot_3]", "Slot 3", "Show the Colors of the Slot 3."],
                ["[Slot_4]", "Slot 4", "Show the Colors of the Slot 4."],
                ["[Slot_5]", "Slot 5", "Show the Colors of the Slot 5."],
                ["-"],
                ["[Slot_All]", "Show All", "Show all the Colors of this Group."],
            ])

        action = ColorsSlotMenu.contextMenu.exec_(globalPos)
        ColorsSlotMenu.slot = ""
        if (not action is None):
            ColorsSlotMenu.slot = action.iconText()

            fileContent = FILE.open(fileName)
            item = fileContent[itemIndex]
            lineData = item.split("|")

            if ("[Slot_" in item):
                lineData[4] = ColorsSlotMenu.slot
            else:
                lineData[4] = ColorsSlotMenu.slot + "|\n"

            fileContent[itemIndex] = '|'.join(lineData)
            FILE.saveList(fileName, fileContent)