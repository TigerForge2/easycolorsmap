from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
from krita import *

# ==== Various Alerts and Prompts managemente =====================================================

class ALERT:
    def __init__(self):
        super().__init__()

    def info(title, text):
        """Show an INFO dialog."""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.exec()
        pass

    def warn(title, text):
        """Show a WARNING dialog."""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.exec()
        pass

    def error(title, text):
        """Show an ERROR dialog."""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.exec()
        pass

    def ask(title, text):
        """Show an QUESTION dialog, with YES/NO buttons."""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msgbox.exec()
        return (reply == QMessageBox.Yes)
        pass

    def prompt(title, text, value = ""):
        """Show a PROMPT dialog that asks for entering a value."""
        msgbox = QInputDialog()
        msgbox.setWindowTitle(title)
        msgbox.setInputMode(QInputDialog.TextInput)
        msgbox.setLabelText(text)
        msgbox.setTextValue(value.replace("\n", ""))

        d = dict()
        if (msgbox.exec()):
            reply = msgbox.textValue()
            if (reply.find("|") >= 0):
                ALERT.error("ATTENTION", "You can't use the '|' (pipe) character inside your text.")
                d["ok"] = False
                d["value"] = ""
            else:
                d["ok"] = True
                d["value"] = reply
        else:
            reply = ""
            d["ok"] = False
            d["value"] = ""

        d["value"] = d["value"].replace("\n", "")
        return d
        pass

    def dialogFileOpen(title, filter):
        """Show an OPEN FILE dialog."""
        msgbox = QFileDialog()
        msgbox.setWindowTitle(title)
        msgbox.setNameFilters([filter])
        if (msgbox.exec()):
            reply = msgbox.selectedFiles()[0]
        else:
            reply = ""

        return reply
        pass

    def ok():
        """Helper: just show an 'OK' message."""
        msgbox = QMessageBox()
        msgbox.setWindowTitle("OK")
        msgbox.setText("ok")
        msgbox.setIcon(QMessageBox.Information)
        msgbox.exec()
        pass

    def log(*message):
        """Helper: show a debug message in the Krita Console."""
        string = ""
        for m in message:
            string += str(m) + " "

        QtCore.qDebug("[LOG]  " + string)