# adapted from https://memotut.com/en/b39165e79d930b9f0fd1/

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *  

import numpy as np

from pathlib import Path

# NGIF functions
import sys, os
try:
    import ngif_romar.tools as tools
except ModuleNotFoundError as error:
    # If not in path/installed, use relative import
    module_path = os.path.abspath(os.path.join("../.."))
    sys.path.append(module_path)
    import ngif_romar.tools as tools


class MyWindow(QMainWindow): # set up the main window widget
    def __init__(self):
        super().__init__() # inherit init
        self.setGeometry(0, 0, 700, 900) # x,y,w,h
        self.setAcceptDrops(True) # drag and drops
        
        self.initUI() # defined below
        
        self.currentScatter = None
        self.lastDir = None
        
        self.droppedFilename = None
    
    def initUI(self):
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget) # put it in centre of the window
        
        layout = QVBoxLayout() # lines up widgets vertically
        centerWidget.setLayout(layout)
        
        self.viewer = gl.GLViewWidget() # basic widget for displaying 3D data
        layout.addWidget(self.viewer, 1) # once you have a layout, you add widgets to it
        
        self.viewer.setWindowTitle('NGIF Data Viewer') # title of the 3D view widget
        self.viewer.setCameraPosition(distance=40) # camera pos (centre , dist, elevation, azumith)
        
        g = gl.GLGridItem() # adds grid plane
        g.setSize(200, 200) # grid size
        g.setSpacing(5, 5) # grid spacing
        self.viewer.addItem(g) # add grid to 3D view

        btn = QPushButton(text="Load Data") # add a load button
        btn.clicked.connect(self.showDialog) # function to be called upon click
        btn.setFont(QFont("Ricty Diminished", 14))
        layout.addWidget(btn)
            
    def showDialog(self): # button functionality
        directory = Path("")
        if self.lastDir: # if there is a previous directory, start from there
            directory = self.lastDir
        fname = QFileDialog.getOpenFileName(self, "Open file", str(directory), "Data file (*.dat)")
        if fname[0]: # if file chosen
            self.showData(fname[0]) # present the data on the grid
            self.lastDir = Path(fname[0]).parent # update last directory

    def showData(self, filename):
        if self.currentScatter: # remove any preexisting scatter
            self.viewer.removeItem(self.currentScatter)

        _, df = tools.read_data(filename) # _ because meta_dict 没有用
        df = tools.post_process_log_data(df)
        # functions here should extract positions and colors
        coords, colours = threeDeePlotVals(df)
        scatter=gl.GLScatterPlotItem(pos=coords, color=colours, size=1)
        scatter.setGLOptions('opaque')
        self.viewer.addItem(scatter)
    
        self.currentScatter=scatter # save current scatter

    # setAcceptDrops is on, so we need to define the drag&drop functions 
    def dragEnterEvent(self, e): # what to do when a drag event is begun
        print("enter")
        mimeData = e.mimeData() # drag and drop data contained in MIME format
        mimeList = mimeData.formats() # types of data in the MIME data
        filename = None
        
        if "text/uri-list" in mimeList: # if there's a universal resource identifier list
            filename = mimeData.data("text/uri-list") # take the list
            filename = str(filename, encoding="utf-8") # convert to UTF8
            filename = filename.replace("file:///", "").replace("\r\n", "").replace("%20", " ") # delete formatting characters
            filename = Path(filename) # convert to path
            
        if filename.exists() and filename.suffix == ".dat":
            e.accept() # accept the drag event; it's relevant
            self.droppedFilename = filename # save the filename
        else:
            e.ignore() # ignore the drag event; it's not relevant
            self.droppedFilename = None
        
    def dropEvent(self, e): # when dropped
        if self.droppedFilename: # if there's a valid filename saved
            self.showData(self.droppedFilename) # load/plot the file

from matplotlib.colors import to_rgba_array
from matplotlib import cm
def threeDeePlotVals(df,partFrame=True,alpha=0.5):
    # get spatial coords
    if partFrame:
        coords=df[['xpart','ypart','zpart']].to_numpy()
    else:
        coords=df[['x','y','z']].to_numpy()

    # now colours. These need to be converted to (N,4) RGBA array
    vals = df['flowWatch'].to_numpy() # extract values
    # normalise values to [0,1]
    if np.unique(vals).shape[0]==1: # if constant
        pass
    else:
        vals=(vals-np.min(vals))/np.ptp(vals) # -min moves lowest val to 0, division by range sets range to 1
    # then convert to colors using a colormap
    cols = cm.plasma(vals) # using the 'jet' colormap
    return coords, to_rgba_array(cols, alpha)

if __name__ == '__main__':
    app = QtGui.QApplication([]) # always need to start a QApplication. _One_ application, no matter how many windows
    window = MyWindow() #
    window.show()
    app.exec_()