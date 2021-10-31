"""
SW 2021-10-29

This is the .py that sorts out the functionality of the plots of single toolpaths

It imports the .ui/.py single_toolpath_plots_ui.py

It will be imported by main_window_ui.py due to use of the promote to button

"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtCore, QtGui, QtWidgets

from single_toolpath_plots_ui import Ui_SingleToolpathPlots

class SingleToolpathPlotsForm(QtWidgets.QWidget, Ui_SingleToolpathPlots):
    def __init__(self, parent=None):
        # As far as I know, and I need to check, some_arg here is the parent widget
        # And it is, checked here
        print("some_arg is {}".format(parent))
        print("some_arg.objectName is {}".format(parent.objectName()))
        super().__init__()
        self.setupUi(parent)
        self.setParent(parent)
        print("Parent is {}".format(self.parent()))
        print("Parent name is {}".format(self.parent().objectName()))

        # This is how we get the layout back in so it fills all of the parent?
        # self.layout = QtWidgets.QGridLayout(self)

        # # Set up other callbacks, etc

        self.plot_fig_tr, self.ax_tr = plt.subplots(tight_layout=True)
        self.plot_widget_tr = FigureCanvas(self.plot_fig_tr)
        layout_tr = QtWidgets.QVBoxLayout(self.plot_tr)
        layout_tr.setContentsMargins(0, 0, 0, 0)
        layout_tr.addWidget(self.plot_widget_tr)

        self.plot_fig_bl, self.ax_bl = plt.subplots(tight_layout=True)
        self.plot_widget_bl = FigureCanvas(self.plot_fig_bl)
        layout_bl = QtWidgets.QVBoxLayout(self.plot_bl)
        layout_bl.setContentsMargins(0, 0, 0, 0)
        layout_bl.addWidget(self.plot_widget_bl)

        self.plot_fig_br, self.ax_br = plt.subplots(tight_layout=True)
        self.plot_widget_br = FigureCanvas(self.plot_fig_br)
        layout_br = QtWidgets.QVBoxLayout(self.plot_br)
        layout_br.setContentsMargins(0, 0, 0, 0)
        layout_br.addWidget(self.plot_widget_br)

