from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
from krita import *
from .ALERT import *
import os.path
from .SYS import *

class FILE:
    def __init__(self):
        super().__init__()
        self.__cutitemindex = -1

    @property
    def cutItemIndex(self):
        return self.__cutitemindex

    @cutItemIndex.setter
    def cutItemIndex(self, value):
        self.__cutitemindex = value

    def save(fileName, data):
        fo = open(fileName, "a")
        fo.write(data + "\n")
        fo.close()

    def saveToIndex(fileName, data, index):
        fileContent = FILE.open(fileName)
        fileContent.insert(index, data + "\n")
        FILE.saveList(fileName, fileContent)

    def saveList(fileName, fileContent):
        fo = open(fileName, "w")
        for item in fileContent:
            if (item != ""): fo.write(item)
        fo.close()

    def write(fileName, data):
        fo = open(fileName, "w")
        fo.write(data)
        fo.close()

    def open(fileName):
        fo = open(fileName, "r")
        lines = fo.readlines()
        fo.close()
        return lines

    def openText(fileName):
        fo = open(fileName, "r")
        lines = fo.read()
        fo.close()
        return lines

    def exists(fileName):
        return (os.path.isfile(fileName))

    def fileTxt(fileName):
        if (fileName.find(".txt") < 0): 
            fileName = fileName + ".txt"
        return fileName
    
    def executeAction(menu, menuItem, index, fileName):

        fileContent = FILE.open(fileName)
        item = fileContent[index]
        lineData = item.split("|")
        isColor = SYS.lineIsColor(item)
        isTitle = SYS.lineIsTitle(item)

        if (menu == menuItem["Rename"] or menu == "[RENAME]"):
            newName = ALERT.prompt("NEW COLOR NAME" if isColor else "NEW GROUP NAME", "Type a new short name:", lineData[0])
            if (newName["ok"]):
                if (isColor):
                    lineData[0] = newName["value"]
                    fileContent[index] = '|'.join(lineData)
                else:
                    fileContent[index] = newName["value"] + "\n"
                FILE.saveList(fileName, fileContent)
            pass

        elif (menu == menuItem["AddTitle"]):
            title = ALERT.prompt("GROUP TITLE", "Type a title for a new group of Colors:")
            if (title["ok"]):
                fileContent.insert(index + 1, title["value"] + "\n")
                FILE.saveList(fileName, fileContent)
            pass

        elif (menu == menuItem["Cut"]):
            FILE.cutItemIndex = index
            pass

        elif (menu == menuItem["Paste"]):
            if (not FILE.isCutIndexValid()):
                ALERT.warn("ATTENTION", "To 'paste' something, you must 'cut' something first.")
                return

            if (index == FILE.cutItemIndex): return
            cutItem = fileContent[FILE.cutItemIndex]
            fileContent[FILE.cutItemIndex] = ""
            fileContent.insert(index + 1, cutItem)
            FILE.saveList(fileName, fileContent)
            FILE.cutItemIndex = -1
            pass

        elif (menu == menuItem["PasteGroup"]):
            if (not FILE.isCutIndexValid()):
                ALERT.warn("ATTENTION", "To 'paste' something, you must 'cut' something first.")
                return
            
            if (isTitle):
                ALERT.error("ATTENTION", "You must click a Color (after which to paste the cut Group). You clicked a Group Title instead.")
                return

            if (SYS.lineIsColor(fileContent[FILE.cutItemIndex])):
                ALERT.error("ATTENTION", "The element you cut was a Color. This 'paste' function can work with cut Groups only.")
                return
            
            group = list()
            for i, line in enumerate(fileContent):
                if (i > FILE.cutItemIndex and SYS.lineIsTitle(line)): break
                if (i >= FILE.cutItemIndex):
                    group.append(line)
                    fileContent[i] = ""

            for i in range(len(group)):
                fileContent.insert(i + (index + 1), group[i])
                ALERT.log(str(i + (index + 1)) + " <- " + group[i])
            
            FILE.saveList(fileName, fileContent)
            FILE.cutItemIndex = -1
            pass

        elif (menu == menuItem["Delete"]):
            del fileContent[index]
            FILE.saveList(fileName, fileContent)
            pass

        elif (menu == "[COLLAPSE]"):
            if (fileContent[index].find(">") == 0):
                fileContent[index] = fileContent[index][1:]
            else:    
                fileContent[index] = ">" + fileContent[index]
            FILE.saveList(fileName, fileContent)
            pass

    def isCutIndexValid():
        if (SYS.isProperty(FILE.cutItemIndex)):
            return False
        elif (FILE.cutItemIndex < 0):
            return False
        return True