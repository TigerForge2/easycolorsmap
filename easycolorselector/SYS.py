from krita import *
from .ALERT import *
import json
import os.path

class SYS:
    def __init__(self):
        super().__init__()

    def currentVersion():
        return 10

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        self.__config = value

    def getVersionString():
        return str(SYS.currentVersion() / 10).replace(",", ".")

    def checkVersion(fileName):
        fileContent = SYS.open(fileName)
        firstLine = fileContent[0]
        update = False
        if (firstLine.find("TF_ECM_FILE") < 0):
            update = True
        else:
            SYS.config = json.loads(firstLine)
            if (SYS.config["version"] < SYS.currentVersion()): update = True

        if (update):
            ALERT.info("COLORS MAP UPDATE", "I'm going to update your Colors Map to the " + SYS.getVersionString() + " version of 'TF Easy Colors Map'.")
            SYS.config = { "version": SYS.currentVersion(), "colorSize": 42, "titleSize" : 24, "colorFontSize": 10, "titleFontSize": 16, "type": "RGB", "scrollSize": 16, "id": "TF_ECM_FILE" }
            fileContent.insert(0, json.dumps(SYS.config) + "\n")
            SYS.saveList(fileName, fileContent)

        pass

    def initMap(fileName):
        SYS.config = { "version": SYS.currentVersion(), "colorSize": 42, "titleSize" : 24, "colorFontSize": 10, "titleFontSize": 16, "type": "RGB", "scrollSize": 16, "id": "TF_ECM_FILE" }
        fileContent = list()
        fileContent.append(json.dumps(SYS.config) + "\n")
        fileContent.append("NEW COLORS MAP\n")
        SYS.saveList(fileName, fileContent)

    def open(fileName):
        fo = open(fileName, "r")
        lines = fo.readlines()
        fo.close()
        return lines

    def saveList(fileName, fileContent):
        fo = open(fileName, "w")
        for item in fileContent:
            if (item != ""): fo.write(item)
        fo.close()

    def configUpdate(fileName):
        fileContent = SYS.open(fileName)
        fileContent[0] = json.dumps(SYS.config) + "\n"
        SYS.saveList(fileName, fileContent)
        pass


    # ==== Utilities ====

    def isProperty(value):
        string = str(value)
        return string.find("property") >= 0

    def lineIsColor(line):
        if (line == "" or line.find("TF_ECM_FILE") > 0): return False
        return (line.find("#") != 0 and line.find("|") > 0)

    def lineIsTitle(line):
        if (line == "" or line.find("TF_ECM_FILE") > 0): return False
        return (line.find("#") < 0 and line.find("|") < 0)