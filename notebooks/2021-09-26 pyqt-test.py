# https://pythonpyqt.com/pyqt-hello-world/
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QToolButton, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


'''#Tutorial 1: an empty window
if __name__ == '__main__':
    app=QApplication(sys.argv) # Each PyQt5 application must create an application object
    w = QWidget() # basic application constructor. Without parent is called a window
    layout = QHBoxLayout() # new horizontal layout; things get added L->R
    btn = QPushButton("Hello World!") # create new button
    layout.addWidget(btn)
    w.setLayout(layout)
    w.resize(250,150) # size in pixels
    w.move(300,300) # screen position, origin = top left
    w.setWindowTitle('Simple')
    w.show()
    sys.exit(app.exec()) # ensures main loop is safely exited (external env can tell master how to end)
'''

"""# Tutorial 2 : a simple push button that closes the window
class PushButton(QWidget): # QWidget is the base class of all user interface objects
    # within this PushButton class we will invoke the QPushButton class to initialise
    # PushButton is a full fledged widget, not quite a button, so we give it QWidget's inheritance
    def __init__(self):
        super().__init__() # retain inheritance of the parent class __init__() function
        self.initUI() # this fn defined below
    
    def initUI(self):
        self.setWindowTitle("PushButton")
        self.setGeometry(400,400,300,260) # a QWidget fn, (x y w h) i.e first 2 are position, second 2 size
        self.closeButton = QPushButton(self) # create the closebutton. This is a method we imported
        self.closeButton.setText("Close")  # add text to that button
        self.closeButton.setIcon(QIcon("close.png")) # and an icon
        self.closeButton.setShortcut('Ctrl+W')  # and a keyboard shortcut
        self.closeButton.clicked.connect(self.close) # define function upon 'clicked' status
        self.closeButton.setToolTip("Close the widget") # add a tool tip
        self.closeButton.move(0,0) # position the button (within window, I presume)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PushButton()
    ex.show()
    sys.exit(app.exec_()) """

# Tutorial 3: a tool button that does not display text but the icon QIcon
class ToolButton(QMainWindow):

    def __init__(self):
        super().__init__() # note in python2 super() requires 2 arguments, e.g. here super(ToolButton, self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ToolButton")
        self.setGeometry(400,400,300,260)

        self.toolbar = self.addToolBar("toolBar") # addToolBar from QMainWindow
        self.statusBar() # creates and returns an empty status bar, or if one already exists then returns it
        # having made the toolbar we'll make a toolbutton object (self._detailsbutton)
        self._detailsbutton = QToolButton() # QToolButton method (imported from PyQT5.QtWidgets)                                     
        self._detailsbutton.setCheckable(True) # whether it cn be marked as clicked (optional property)                                 
        self._detailsbutton.setChecked(False) # initially, not clicked                                   
        self._detailsbutton.setArrowType(Qt.RightArrow) # set type of arrow displayed on the buttton
        self._detailsbutton.setAutoRaise(True) # automatically raise the button. Options: NoArrow,Up/Down/Left/RightArrow
        #self._detailsbutton.setIcon(QIcon("test.jpg"))
        self._detailsbutton.setToolButtonStyle(Qt.ToolButtonIconOnly) # sets style of button text and display. Her we've chosen icon and not text. 
        # Could also choose: IconOnly,TextOnly,TextBesideIcon,TextUnderIcon,FollowStyle
        self._detailsbutton.clicked.connect(self.showDetail) # when clicked, call the showDetail function we'll define below
        self.toolbar.addWidget(self._detailsbutton) # add self._detailsbutton to the toolbar

    def showDetail(self):
        if self._detailsbutton.isChecked():
            self.statusBar().showMessage("Show Detail....")
        else:
            self.statusBar().showMessage("Close Detail....")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ToolButton()
    ex.show()
    sys.exit(app.exec_())
