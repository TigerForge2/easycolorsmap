from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from krita import *

class HELP(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.fileName = ""

        self.setFixedWidth(640)    
        self.setFixedHeight(480)    
        self.setWindowTitle("TF Easy Colors Map » GUIDE")

        HTML = ""
        HTML += "<h2>TF Easy Colors Map - GUIDE</h2>"
        HTML += "<br><table>"
        HTML += "<tr>"
        HTML += "<td><b>QUICK REFERENCE</b></td>"
        HTML += "<td></td>"
        HTML += "<td></td>"
        HTML += "</tr>"
        HTML += "<tr>"
        HTML += "<td><b>LEFT</b> click</td>"
        HTML += "<td></td>"
        HTML += "<td>&nbsp;&nbsp;Set the <b>foreground</b> color</td>"
        HTML += "</tr>"
        HTML += "<tr>"
        HTML += "<td><b>LEFT</b> click</td>"
        HTML += "<td>+ <b>SHIFT</b></td>"
        HTML += "<td>&nbsp;&nbsp;Set the <b>background</b> color</td>"
        HTML += "</tr>"
        HTML += "<tr>"
        HTML += "<td><b>LEFT</b> click</td>"
        HTML += "<td>+ <b>CTRL</b></td>"
        HTML += "<td>&nbsp;&nbsp;Change the clicked Color or Group Title name</td>"
        HTML += "</tr>"
        HTML += "<tr>"
        HTML += "<td><b>RIGHT</b> click</td>"
        HTML += "<td></td>"
        HTML += "<td>&nbsp;&nbsp;Add a new color (at the end of the Map)</td>"
        HTML += "</tr>"
        HTML += "<tr>"
        HTML += "<td><b>RIGHT</b> click</td>"
        HTML += "<td>+ <b>SHIFT</b></td>"
        HTML += "<td>&nbsp;&nbsp;Add a new color <b>after</b> the clicked Color or Group Title</td>"
        HTML += "</tr>"
        HTML += "<tr>"
        HTML += "<td><b>RIGHT</b> click</td>"
        HTML += "<td>+ <b>CTRL</b></td>"
        HTML += "<td>&nbsp;&nbsp;Show a popup menu with some functionalities</td>"
        HTML += "</tr>"
        HTML += "</table><br><br>"
        HTML += "<b>Create or load a Colors Map</b><br>"
        HTML += "Press the 'Open Map' button. Type a new file name to create a new Colors Map or select and open an existing Colors Map.<br>Note that a Colors Map file is just a simple .txt file."
        HTML += "<br><br>"
        HTML += "<b>Add a new color</b><br>"
        HTML += "With a Krita document opened and the desired color set as <b>foreground</b> color, just <b>right</b> click on the Map panel. Type a short name for the color and press [OK] (if you press [CANCEL] no color is added)."
        HTML += "<br><br>"
        HTML += "<b>Add a new color in a specific position</b><br>"
        HTML += "Follow the instructions above, but <b>right</b> click + <b>SHIFT</b> button on an existing color. The new color will be added <b>after</b> that color.<br>Note that you can click a Group Title to add the color as first color."
        HTML += "<br><br>"
        HTML += "<b>Add new colors automatically</b><br>"
        HTML += "Press the 'Auto Add Colors' button. Every time you change the <b>foreground</b> color, the new color is automatically added to the Map. Press again the 'Auto Add Colors' button to stop this functionality.<br>Note that the new colors are added at the end of the Map."
        HTML += "<br><br>"
        HTML += "<b>Select a Color of the Map</b><br>"
        HTML += "<b>Left</b> click an existing color: it will set the Krita document <b>foreground</b> color.<br>"
        HTML += "<b>Left</b> click + <b>SHITF</b> button an existing color: it will set the Krita document <b>background</b> color."
        HTML += "<br><br>"
        HTML += "<b>Colors Management (rename, move, delete, etc.)</b><br>"
        HTML += "<b>Right</b> click + <b>CTRL</b> button an existing Color or Title: a popup menu will apear with the available functionalities."
        HTML += "<br><br>"
        HTML += " - <b>Add Group Title:</b> add a new Group Title <b>after</b> the clicked Color or Title.<br>" 
        HTML += " - <b>Rename:</b> change the name of the clicked Color or Title (you can also left click + CTRL the item to rename).<br>" 
        HTML += " - <b>Cut:</b> select a Color or a Title for a successive 'paste' operation.<br>" 
        HTML += " - <b>Paste:</b> move a Color or a Title <b>after</b> the clicked <b>color</b> (you must click a Color).<br>" 
        HTML += " - <b>Paste Group:</b> move a Group Title and all the Colors under it <b>after</b> the clicked <b>color</b> (you must click a Color).<br>" 
        HTML += " - <b>Delete:</b> delete the clicked Color or Title (the Group Title only will be deleted, not the Colors under it)." 
        HTML += "<br><br>"
        HTML += "<b>Temporary Colors (Secondary palette)</b><br>"
        HTML += "If you want to collect some color, but you don't want to save them into your Colors Map, you can add colors to the palette under the Colors Map. Just right click to add colors and left click for setting the foreground color (+SHIFT for setting the background instead)."
        HTML += "<br><br>"
        HTML += "<b>Settings</b><br>"
        HTML += "Press the 'Settings' button. A window will appear showing supported settings.<br>"
        HTML += " - <b>Set Color size:</b> allow to change the size of the Color boxes.<br>" 
        HTML += " - <b>Set Color Name size:</b> allow to change the size of the name inside the Color boxes." 
        HTML += "<br><br>"
        HTML += "<br><br>"
        HTML += "<b>Colors Map Editor</b><br>"
        HTML += "Press the 'Map Editor' button. A window will appear showing the content of the Colors Map file. You can manually perform modifications and save the Map.<br>Use this functionality with caution."
        HTML += "<br><br>"

        textArea = QTextEdit(self)
        textArea.setReadOnly(True)
        textArea.setHtml(HTML)
        
        layout.addWidget(textArea)
        self.setLayout(layout)

