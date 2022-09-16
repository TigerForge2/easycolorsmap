import os
import os.path

# ==== File operations management =================================================================

class FILE:
    def __init__(self):
        super().__init__()

    # ---- Opening data ---------------------------------------------------------------------------

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

    # ---- Saving data ----------------------------------------------------------------------------

    def save(fileName, data):
        """Save a string data into a file."""
        fo = open(fileName, "w")
        fo.write(data)
        fo.close()

    def append(fileName, data):
        """Append a string data at the end of a file ('new line' is included)."""
        fo = open(fileName, "a")
        fo.write(data + "\n")
        fo.close()

    def saveToIndex(fileName, data, index):
        """Insert a string in the specified index position ('new line' is included)."""
        fileContent = FILE.open(fileName)
        fileContent.insert(index, data + "\n")
        FILE.saveList(fileName, fileContent)

    def saveList(fileName, fileContent, addNewLine = False, excludeEmptyStrings = True):
        """Save a List into a file. The 'new line' inclusion is controlled by the addNewLine param. By default, empty strings are not saved (controlled by excludeEmptyStrings param)."""
        fo = open(fileName, "w")
        newLine = "\n" if addNewLine else ""
        for item in fileContent:
            if (excludeEmptyStrings):
                if (item != ""): fo.write(item + newLine)
            else:
                fo.write(item + newLine)
        fo.close()

    # ---- Special operations ---------------------------------------------------------------------
    
    def modifyLine(fileName, lineIndex, position, value):
        """Open the file, get the line at lineIndex, split it, change the value at the given position, finally save the file."""
        fileContent = FILE.open(fileName)
        line = fileContent[lineIndex].split("|")
        line[position] = value
        fileContent[lineIndex] = '|'.join(line)
        FILE.saveList(fileName, fileContent)

    def modifyLineToggle(fileName, lineIndex, position, value1, value2):
        """Open the file, get the line at lineIndex, split it, change the value at the given position (using a toggle logic between value1 and value2), finally save the file."""
        fileContent = FILE.open(fileName)
        line = fileContent[lineIndex].split("|")
        line[position] = value1 if line[position] == value2 else value2
        fileContent[lineIndex] = '|'.join(line)
        FILE.saveList(fileName, fileContent)

    def extractLine(fileName, lineIndex):
        """Open the file and return the line at lineIndex."""
        fileContent = FILE.open(fileName)
        return fileContent[lineIndex]

    # ---- Specific Groups / Colors operations ----------------------------------------------------

    def getGroupsList(fileName):
        """Return the list of Groups from the given Colors Map."""
        fileContent = FILE.open(fileName)
        groups = list()
        for item in fileContent:
            if (item.find("[G]") == 0): groups.append(item)

        return groups

    def getColorsList(fileName):
        """Return the list of Colors from the given Colors Map."""
        fileContent = FILE.open(fileName)
        groups = list()
        for item in fileContent:
            if (item.find("[C]") == 0): groups.append(item)

        return groups

    def changeLineValue(line, position, value):
        """Split a line, change the value at the given position, then ricreate the line."""
        data = line.split("|")
        data[position] = value
        return "|".join(data)

    def getLineValue(line, position):
        """Split a line and return the value at the given position"""
        data = line.split("|")
        return data[position]

    # ---- Helpers --------------------------------------------------------------------------------

    def exists(fileName):
        """Return True if the file exists"""
        return (os.path.isfile(fileName))

    def notExists(fileName):
        """Return True if the file doesn't exist"""
        return not(os.path.isfile(fileName))

    def getExtension(fileName):
        """Return the Extension of the given file"""
        return os.path.splitext(fileName)[1]

    def checkExtension(fileName, extension):
        """Return True if the given file Extension is equal to the given Extension (it must contain .)"""
        return os.path.splitext(fileName)[1] == extension

    def currentFilePath(target):
        """Return the file's current path. Given target should be: __file__"""
        return os.path.dirname(os.path.abspath(target))

    def getCurrentPathToFile(target, fileName):
        """Return the file's current path combined with the given fileName. Given target should be: __file__"""
        path = os.path.dirname(os.path.abspath(target))
        return os.path.join(path, fileName)