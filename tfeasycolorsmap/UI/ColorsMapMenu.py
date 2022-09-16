from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

from krita import *

from .Tools import *
from ..Core.FILE import *
from ..Core.ALERT import *

# **** Colors Maps management *********************************************************************

class ColorsMapMenu:

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
    def cutItemIndex(self):
        return self.__cutItemIndex

    @cutItemIndex.setter
    def cutItemIndex(self, value):
        self.__cutItemIndex = value

    @property
    def cutItemType(self):
        return self.__cutItemType

    @cutItemType.setter
    def cutItemType(self, value):
        self.__cutItemType = value

    def __init__(self):
        super().__init__()

    def show(globalPos, itemIndex, fileName):
        ColorsMapMenu.contextMenu = Tools.contextMenu()
        ColorsMapMenu.contextMenuItems = Tools.contextMenuItems(
            ColorsMapMenu.contextMenu,
            [
                ["AddGroup", "Add Group Title", "Add a Group Title after this clicked Color or Group."],
                ["Rename", "Rename [left + CTRL]", "Change the name of the clicked Color or Group."],
                ["-"],
                ["Cut", "Cut", "Select the clicked Color or Group  for the next 'Paste' operation."],
                ["Paste", "Paste after", "Paste the 'cut' element after this clicked Color or Group."],
                ["PasteGroup", "Paste Group after", "Paste the 'cut' Group and all its Colors after the clicked Color."],
                ["-"],
                ["Delete", "Delete", "Delete the clicked Color or Group (not its Colors)"],
                ["DeleteGroup", "Delete Group", "Delete the clicked Group and all its Colors."]
            ])

        action = ColorsMapMenu.contextMenu.exec_(globalPos)
        if (not action is None): ColorsMapMenu.execute(action.iconText(), itemIndex, fileName)

    def execute(action, index, fileName):
        fileContent = FILE.open(fileName)
        item = fileContent[index]
        lineData = item.split("|")
        isColor = lineData[0] == "[C]"
        isGroup = lineData[0] == "[G]"

        if (action == "AddGroup"):

            title = ALERT.prompt("GROUP TITLE", "Type a title for a new group of Colors:")
            if (title["ok"]):
                fileContent.insert(index + 1, "[G]|[O]|[V]|" + title["value"] + "|" + "\n")
                FILE.saveList(fileName, fileContent)

        elif (action == "Rename"):
            
            newName = ALERT.prompt("NEW COLOR NAME" if isColor else "NEW GROUP NAME", "Type a new short name:", lineData[3])
            if (newName["ok"]):
                lineData[3] = newName["value"]
                fileContent[index] = '|'.join(lineData)
                FILE.saveList(fileName, fileContent)

        elif (action == "Cut"):
            
            ColorsMapMenu.cutItemIndex = index
            ColorsMapMenu.cutItemType = lineData[0]

        elif (action == "Paste"):

            if (not ColorsMapMenu.isCutIndexValid()): 
                ALERT.warn("ATTENTION", "To 'paste' something, you must 'cut' something first.")
                return
            if (index == ColorsMapMenu.cutItemIndex):
                ALERT.warn("ATTENTION", "You can't 'paste' on the same item you have just 'cut'.")
                return
            if (ColorsMapMenu.cutItemIndex == 1):
                ALERT.warn("ATTENTION", "You can't 'cut/paste' the first Group without moving also its Colors. Use 'Paste Group' in this case.")
                return
            if (ColorsMapMenu.cutItemType == "[G]" and isGroup):
                ALERT.warn("ATTENTION", "You can't 'paste' a Group after another Group. Click and 'paste' after a Color instead.")
                return

            cutItem = fileContent[ColorsMapMenu.cutItemIndex]
            fileContent[ColorsMapMenu.cutItemIndex] = ""
            fileContent.insert(index + 1, cutItem)
            FILE.saveList(fileName, fileContent)
            ColorsMapMenu.cutItemIndex = -1
            
        elif (action == "PasteGroup"):

            if (not ColorsMapMenu.isCutIndexValid()): 
                ALERT.warn("ATTENTION", "To 'paste' something, you must 'cut' something first.")
                return
            if (index == ColorsMapMenu.cutItemIndex):
                ALERT.warn("ATTENTION", "You can't 'paste' on the same item you have just 'cut'.")
                return
            if (ColorsMapMenu.cutItemType == "[C]"):
                ALERT.error("ATTENTION", "The element you cut was a Color. This 'paste' function can work with cut Groups only.")
                return
            if (isGroup):
                ALERT.error("ATTENTION", "You can't 'paste' a Group after another Group. Click and 'paste' after a Color instead.")
                return

            group = list()
            for i, line in enumerate(fileContent):
                if (i > ColorsMapMenu.cutItemIndex and ColorsMapMenu.lineIsGroup(line)): break
                if (i >= ColorsMapMenu.cutItemIndex):
                    group.append(line)
                    fileContent[i] = ""

            for i in range(len(group)):
                fileContent.insert(i + (index + 1), group[i])
            
            FILE.saveList(fileName, fileContent)
            ColorsMapMenu.cutItemIndex = -1
            
        elif (action == "Delete"):
            
            del fileContent[index]
            FILE.saveList(fileName, fileContent)

        elif (action == "DeleteGroup"):

            if (isColor):
                ALERT.error("ATTENTION", "You can't 'delete' a Color with this function.")
                return

            if (ALERT.ask("ATTENTION", "This operation will delete this Group and all its Colors.\n\nAre you sure?")):
                deleteColors = False
                for i, line in enumerate(fileContent):
                    
                    if (deleteColors and ColorsMapMenu.lineIsColor(line)):
                        fileContent[i] = ""

                    if (ColorsMapMenu.lineIsGroup(line)):
                        deleteColors = False

                    if (i == index):
                        fileContent[i] = ""
                        deleteColors = True

                FILE.saveList(fileName, fileContent)


    def isCutIndexValid():
        if (Tools.isProperty(ColorsMapMenu.cutItemIndex)):
            return False
        elif (ColorsMapMenu.cutItemIndex < 0):
            return False
        return True

    def lineIsColor(line):
        return (line.find("[C]") == 0)

    def lineIsGroup(line):
        return (line.find("[G]") == 0)