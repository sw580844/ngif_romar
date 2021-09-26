# https://pythonpyqt.com/pyqt-hello-world/
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

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
