"""
2021-09-24 Quick Pyside/QT POC

Also check https://stackoverflow.com/questions/43947318/plotting-matplotlib-figure-inside-qwidget-using-qt-designer-form-and-pyqt5
to make sure the process for taking a blank widget and turning into a matplotlib plot is appropriate

Also page 168/178 of matplotlib for python developers

"""


import re
import sys
import os
import argparse
from pathlib import Path
import pandas as pd

#from PySide2.QtWidgets import QApplication, QMainWindow
#from PySide2 import QtWidgets
# from PySide2.QtCore import QFile

# PyQt stuff (Scott uses Pyside, commented out above)
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi
import pyqtgraph.opengl as gl


# Extra includes so py2exe picks them up, presumably this can be done elsehwere
import cv2
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba_array
from matplotlib import cm

from main_window_ui import Ui_MainWindow

try:
    from ngif_romar import tools
except ModuleNotFoundError as error:
    # If not in path/installed, use relative import
    module_path = os.path.abspath(os.path.join("../ngif_romar"))
    # hard coded
    #module_path = r"C:\Users\uqthirsc\Repos\Code\ngif_romar"
    sys.path.append(module_path)
    from ngif_romar import tools





class MatplotlibWidget(FigureCanvas):
    """
    Basic class to make a widget from a matlplotlib figure
    """

    def __init__(self, parent=None,xlabel='x',ylabel='y',title='Title'):
        super(MatplotlibWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)



# Also try https://stackoverflow.com/questions/6723527/getting-pyside-to-work-with-matplotlib
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window of POC app
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Set up callbacks
        self.open_file_button.clicked.connect(self.load_file)
        self.make_plots_button.clicked.connect(self.make_plots)
        self.pushButton_make_toolpath_plots.clicked.connect(self.make_toolpath_plots)
        self.combo_box_select_page.currentIndexChanged.connect( # change page to the value stored in the combo box
            self.stackedWidget.setCurrentIndex
        )
        self.preprocess_file_checkbox.stateChanged.connect(self.reload_file) # reload if preprocess status changed

        # Default stacked: zero page
        self.stackedWidget.setCurrentIndex(0)
        # Arbitrary plotting buttons etc
        self.page3_pushbutton_repopulate.clicked.connect(self.populate_arb_var_combo_boxes)
        self.page3_pushbutton_makeplots.clicked.connect(self.make_arb_var_plots)
        # 3D plot button
        self.page4_pushbutton_makeplot.clicked.connect(self.make_3D_plot)


        # Parse command line. TBD whether there's a better way to mix stock python and Qt
        parser = argparse.ArgumentParser()
        parser.add_argument("--default_data_dir", help="Default data location")
        parser.add_argument("--default_data_file", help="Default data file to open at start")
        args = parser.parse_args()
        # If default data file specified, load in to start
        if args.default_data_file:
            if not os.path.exists(os.path.abspath(args.default_data_file)):
                print("Default data file specified but does not exist: '{}'".format(
                    self.default_data_file))
                raise ValueError
            self.load_and_proc_file(
                os.path.abspath(args.default_data_file), preprocess=True
            )
        else:
            self.log_data_df = None

        # Handle default data dir if specified
        if args.default_data_dir and not args.default_data_file:
            self.default_data_dir = os.path.abspath(args.default_data_dir)
            if not os.path.exists(self.default_data_dir):
                print("Default data dir specified but does not exist: '{}'".format(
                    self.default_data_dir))
                raise ValueError
        elif args.default_data_file:
            self.default_data_dir = os.path.dirname(os.path.abspath(args.default_data_file))
        else:
            self.default_data_dir = None
 
        self.setup_plot_areas()

        self.currentScatter = None # gl scatter object, initially blank
        self.lastDir = None # last visited directory, for reference when loading files
        self.lastFile = None # last loaded file, for reloading

    def setup_plot_areas(self):
        """
        Catch all function to set up all the plot areas

        It would be nice to do this in a more elegant way
        """

        # Create a default plot
        self.plot_fig_1, self.ax1 = plt.subplots(tight_layout=True)
        self.plotWidget_1 = FigureCanvas(self.plot_fig_1)

        # Here turn each of the QWidget plot areas we created into the designer into a layout, and
        # First 3 layouts are the three timeseries plots on page 1    
        p1topright = QtWidgets.QVBoxLayout(self.page1_topright) # this is the line that links handwritten code to the QtDesigner code (widget_PlotArea_1 is from the designer)
        p1topright.setContentsMargins(0, 0, 0, 0)
        p1topright.addWidget(self.plotWidget_1)

        # Create a default plot
        self.plot_fig_2, self.ax2 = plt.subplots(tight_layout=True)
        self.plotWidget_2 = FigureCanvas(self.plot_fig_2)

        # Here turn each of the QWidget plot areas we created into the designer into a layout, and
        p1bottomright = QtWidgets.QVBoxLayout(self.page1_bottomright)
        p1bottomright.setContentsMargins(0, 0, 0, 0)
        p1bottomright.addWidget(self.plotWidget_2)

        # Create a default plot
        self.plot_fig_3, self.ax3 = plt.subplots(tight_layout=True)
        self.plotWidget_3 = FigureCanvas(self.plot_fig_3)

        # Here turn each of the QWidget plot areas we created into the designer into a layout, and
        p1bottomleft = QtWidgets.QVBoxLayout(self.page1_bottomleft)
        p1bottomleft.setContentsMargins(0, 0, 0, 0)
        p1bottomleft.addWidget(self.plotWidget_3)

        # Toolpath plots
        # Organisation: Put toolpath fig, ax into a dict (fig, ax)
        self.toolpath_plots_dict = {
            "poolsize_per_toolpath" : plt.subplots(tight_layout=True),
            "pooltemp_per_toolpath" : plt.subplots(tight_layout=True),
            "flowwatch_per_toolpath" : plt.subplots(tight_layout=True),
        }
        self.toolpath_canvas_dict = {
            "poolsize_per_toolpath" : FigureCanvas(
                self.toolpath_plots_dict["poolsize_per_toolpath"][0]),
            "pooltemp_per_toolpath" : FigureCanvas(
                self.toolpath_plots_dict["pooltemp_per_toolpath"][0]),
            "flowwatch_per_toolpath" : FigureCanvas(
                self.toolpath_plots_dict["flowwatch_per_toolpath"][0]),
        }

        p2bottomleft = QtWidgets.QVBoxLayout(self.page2_bottomleft)
        p2bottomleft.setContentsMargins(0, 0, 0, 0)
        p2bottomleft.addWidget(self.toolpath_canvas_dict["poolsize_per_toolpath"])

        p2bottomright = QtWidgets.QVBoxLayout(self.page2_bottomright)
        p2bottomright.setContentsMargins(0, 0, 0, 0)
        p2bottomright.addWidget(self.toolpath_canvas_dict["pooltemp_per_toolpath"])

        p2topright = QtWidgets.QVBoxLayout(self.page2_topright)
        p2topright.setContentsMargins(0, 0, 0, 0)
        p2topright.addWidget(self.toolpath_canvas_dict["flowwatch_per_toolpath"])

        # Arbitrary var plotting
        # Objects will be fig, ax, canvas
        self.arb_var_plotting_objects = list(plt.subplots(tight_layout=True))
        self.arb_var_plotting_objects.append(
            FigureCanvas(self.arb_var_plotting_objects[0])
        )
        p3bottomright = QtWidgets.QVBoxLayout(self.page3_bottomright)
        p3bottomright.setContentsMargins(0, 0, 0, 0)
        p3bottomright.addWidget(self.arb_var_plotting_objects[2])   

        ## 3D plot
        # add layout
        p4centre = QtWidgets.QVBoxLayout(self.page4_centre) # layout of the 3D plot widget
        # add gl viewer to layout
        self.viewer = gl.GLViewWidget() # basic widget for displaying 3D data
        p4centre.addWidget(self.viewer, 1) # add widget to layout
        self.viewer.setWindowTitle('NGIF Data Viewer') # title of the 3D view widget
        self.viewer.setCameraPosition(distance=40) # camera pos (centre , dist, elevation, azumith)
        # add grid to the viewer
        g = gl.GLGridItem()
        g.setSize(200,200)
        g.setSpacing(5,5)
        self.viewer.addItem(g)
        return

    def make_3D_plot(self):
        """
        Generate interactive 3D plot
        """
        # clear gl of preexisting scatter
        if self.currentScatter: # remove any preexisting scatter
            self.viewer.removeItem(self.currentScatter)
        # load data, removing laser off sections if desired
        if self.log_data_df is None:
            print("Log Data df empty")
            return
        plot_subset = self.log_data_df
        if bool(self.page4_checkBox_laseron.checkState()):
            plot_subset = plot_subset[
                plot_subset["laser_on_time(ms)"] > 200
            ]
        else:
            pass
        
        coords, colours = self.threeDeePlotVals(plot_subset)
        scatter=gl.GLScatterPlotItem(pos=coords, color=colours, size=1)
        scatter.setGLOptions('opaque')
        self.viewer.addItem(scatter)
    
        self.currentScatter=scatter # save current scatter
        return

    def threeDeePlotVals(df,partFrame=True,alpha=0.5):
        """
        Generates coordinates and colours for gl scatterplot from dataframe
        24/10/21 TODO: currently hard coded to FlowWatch for demo purposes
        """
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


    def make_arb_var_plots(self):
        """
        Generate the arbitrary variable plots
        """
        if self.log_data_df is None:
            print("Log Data df empty")
            return
        plot_subset = self.log_data_df
        if bool(self.page3_checkbox_laser_on.checkState()):
            plot_subset = plot_subset[
                plot_subset["laser_on_time(ms)"] > 200
            ]
        else:
            pass

        columns = self.log_data_df.keys()
        x_col = columns[self.combo_box_arb_var_x.currentIndex()]
        y_col = columns[self.combo_box_arb_var_y.currentIndex()]

        ax = self.arb_var_plotting_objects[1]
        ax.cla()
        ax.plot(plot_subset[x_col], plot_subset[y_col])
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        self.arb_var_plotting_objects[2].draw()
        return


    def make_toolpath_plots(self):
        """
        Create the per toolpath plots

        TODO: Issue, preprocess should have been on for toolpaths? Check?
        """
        if self.log_data_df is None:
            print("Log Data df empty")
            return
        if "toolpath_key" not in self.log_data_df.keys():
            print("ISSUE: Toolpath key not present in datafile")
            return

        # Subset out the toolpath key -1, which corresponds to those points with laser off
        subset = self.log_data_df[
            self.log_data_df["toolpath_key"] != -1
        ]
        groupby_mean = subset.groupby("toolpath_key").mean().reset_index()
        groupby_std = subset.groupby("toolpath_key").std().reset_index()

        ax = self.toolpath_plots_dict["poolsize_per_toolpath"][1]
        ax.cla()
        ax.plot(groupby_mean["toolpath_key"], groupby_mean["meltpoolSize"], label="Mean value")
        ax.plot(
            groupby_mean["toolpath_key"],
            groupby_mean["meltpoolSize"] - groupby_std["meltpoolSize"],
            linestyle="--", label="Mean - $\\sigma$"
        )
        ax.plot(
            groupby_mean["toolpath_key"],
            groupby_mean["meltpoolSize"] + groupby_std["meltpoolSize"],
            linestyle="--", label="Mean + $\\sigma$"
        )
        ax.legend()
        ax.set_xlabel("Toolpath key")
        ax.set_ylabel("Meltpool size(pix)")
        ax.set_title("Meltpool size per toolpath")
        self.toolpath_canvas_dict["poolsize_per_toolpath"].draw()

        ax = self.toolpath_plots_dict["pooltemp_per_toolpath"][1]
        ax.cla()
        ax.plot(groupby_mean["toolpath_key"], groupby_mean["meltpoolTemp"], label="Mean value")
        ax.plot(
            groupby_mean["toolpath_key"],
            groupby_mean["meltpoolTemp"] - groupby_std["meltpoolTemp"],
            linestyle="--", label="Mean - $\\sigma$"
        )
        ax.plot(
            groupby_mean["toolpath_key"],
            groupby_mean["meltpoolTemp"] + groupby_std["meltpoolTemp"],
            linestyle="--", label="Mean + $\\sigma$"
        )
        ax.legend()
        ax.set_xlabel("Toolpath key")
        ax.set_ylabel("Meltpool temp(degC?)")
        ax.set_title("Meltpool temp per toolpath")
        self.toolpath_canvas_dict["pooltemp_per_toolpath"].draw()

        ax = self.toolpath_plots_dict["flowwatch_per_toolpath"][1]
        ax.cla()
        ax.plot(groupby_mean["toolpath_key"], groupby_mean["flowWatch"], label="Mean value")
        ax.plot(
            groupby_mean["toolpath_key"],
            groupby_mean["flowWatch"] - groupby_std["flowWatch"],
            linestyle="--", label="Mean - $\\sigma$"
        )
        ax.plot(
            groupby_mean["toolpath_key"],
            groupby_mean["flowWatch"] + groupby_std["flowWatch"],
            linestyle="--", label="Mean + $\\sigma$"
        )
        ax.legend()
        ax.set_xlabel("Toolpath key")
        ax.set_ylabel("Flow watch sensor (AU)")
        ax.set_title("Flow watch per toolpath")
        self.toolpath_canvas_dict["flowwatch_per_toolpath"].draw()

        return


    def make_plots(self):
        """
        Callback function to make plots, assumes data df has been loaded in but squashes this error
        """
        if self.log_data_df is None:
            print("Log data df empty")
            return

        plot_subset = self.log_data_df
        if bool(self.plot_laser_on.checkState()):
            plot_subset = plot_subset[
                plot_subset["laser_on_time(ms)"] > 200
            ]
        else:
            pass
        # Putting into ms bc we can't have fraction rolling at this stage
        rolling_mean_window = int(self.rolling_window_seconds.value() * 1000)
        if rolling_mean_window > 0.1:
            # Figure out how to do without redoing index
            # Note, pandas rolling has a backwards facing window, and resample has an even window
            # https://pandas.pydata.org/pandas-docs/version/1.1.5/user_guide/computation.html
            # Rework, warning about setting values on copy of slice
            plot_subset["t_datetime"] = pd.to_datetime(plot_subset["t"], unit="ms")
            # plot_subset = plot_subset.set_index(plot_subset["t_datetime"])
            plot_subset = plot_subset.rolling(
                "{}ms".format(rolling_mean_window), on="t_datetime"
            ).mean()

        if not bool(self.preprocess_file_checkbox.checkState()): # if not preprocessing, we won't have access to t (min) and must plot in milliseconds
            xcolumn = "t"
            xlabel = "Time (ms)"
        else:
            xcolumn = "t(min)"
            xlabel = "Time (min)"

        self.ax1.cla()
        self.ax1.plot(plot_subset[xcolumn], plot_subset["meltpoolSize"])
        self.ax1.set_xlabel(xlabel)
        self.ax1.set_ylabel("Meltpool size (pix)")
        self.ax1.set_title("Meltpool size over time")
        # self.plot_fig_1.tight_layout()
        self.plotWidget_1.draw()

        self.ax2.cla()
        self.ax2.plot(plot_subset[xcolumn], plot_subset["flowWatch"])
        self.ax2.set_xlabel(xlabel)
        self.ax2.set_ylabel("Flow watch sensor (AU)")
        self.ax2.set_title("Flow watch sensor over time")
        # self.plot_fig_2.tight_layout()
        self.plotWidget_2.draw()

        self.ax3.cla()
        self.ax3.plot(plot_subset[xcolumn], plot_subset["protectionGlasTemperature"])
        self.ax3.set_xlabel(xlabel)
        self.ax3.set_ylabel("Protection glass temp (degC)")
        self.ax3.set_title("Protection glass temperature")
        # self.plot_fig_3.tight_layout()
        self.plotWidget_3.draw()

        return

    def reload_file(self):
        """
        Used to reload data, when preprocess checkbox status changes
        """
        if self.lastFile: # if previous file exists
            preprocess = bool(self.preprocess_file_checkbox.checkState())
            self.load_and_proc_file(self.lastFile, preprocess)
        
        return

    def load_file(self):
        """
        Used to open up the file selector to find path to data file, and then calls
        load_and_proc_file to load it in
        """
        # Use dir to set default folder
        directory = Path("")
        if self.lastDir: # if previous directory, start from there
            directory = self.lastDir
    
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", str(directory), "Data file (*.dat)")
        preprocess = bool(self.preprocess_file_checkbox.checkState())
    
        if file_path: # if file chosen
            print("file_path is {}".format(file_path))
            self.lastDir = Path(file_path).parent
            self.lastFile = Path(file_path) # save filepath for reloading
            self.load_and_proc_file(file_path, preprocess)

        return

    def load_and_proc_file(self, file_path, preprocess):
        """
        Given path to data file, loads and optionally preprocesses using methods in ngif_romar.tools
        """
        print("Reading data")
        self.metadata_dict, self.log_data_df = tools.read_data(file_path)
    
        if preprocess:
            print("Preprocessing")
            self.log_data_df = tools.post_process_log_data(self.log_data_df)

    def populate_arb_var_combo_boxes(self):
        """
        This readjusts the comboboxes according to what columns are available in the data df
        """

        if self.log_data_df is None:
            print("Log data df empty")
            return


        columns = self.log_data_df.keys()

        self.combo_box_arb_var_x.clear()
        self.combo_box_arb_var_x.addItems(columns)
        self.combo_box_arb_var_y.clear()
        self.combo_box_arb_var_y.addItems(columns)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
