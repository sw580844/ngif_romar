"""
2021-09-24 Quick Pyside/QT POC

Also check
https://stackoverflow.com/questions/43947318/plotting-matplotlib-figure-inside-qwidget-using-qt-designer-form-and-pyqt5
to make sure the process for taking a blank widget and turning into a matplotlib plot is
appropriate

Also page 168/178 of matplotlib for python developers

TODO: Check https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html and other sources
for better ways of incorporating custom widgets in designer

2021-11-02
Single toolpath plots are placed in their own widget

"""


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
    QApplication, QMainWindow
)
from PyQt5 import QtGui
import pyqtgraph as pg
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

from single_toolpaths_plots_code import SingleToolpathPlotsForm


try:
    from ngif_romar import tools
except ModuleNotFoundError as error:
    # If not in path/installed, use relative import
    module_path = os.path.abspath(os.path.join("."))
    sys.path.append(module_path)
    from ngif_romar import tools





class MatplotlibWidget(FigureCanvas):
    """
    Basic class to make a widget from a matlplotlib figure
    """

    def __init__(self, parent=None,xlabel='x',ylabel='y',title='Title'):
        # super(MatplotlibWidget, self).__init__(Figure())
        super().__init__(Figure())

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
        # super(MainWindow, self).__init__()
        super().__init__()
        self.setupUi(self)

        # Set up some basic values, here mostly so that last_file can be picked up by
        # reload_file
        # self.currentScatter = None # gl scatter object, initially blank
        self.last_dir = None # last visited directory, for reference when loading files
        self.last_file = None # last loaded file, for reloading
        self.page4_column = None # desired column to plot in 3D plotting
        self.current_scatter = None # gl scatter object, initially blank

        # Set main window icon
        self.setWindowIcon(QtGui.QIcon(os.path.join("ui", "romar_r.png")))

        # Set up callbacks
        self.open_file_button.clicked.connect(self.load_file)
        self.make_plots_button.clicked.connect(self.make_plots)
        self.page1_pushbutton_save_summary_plots.clicked.connect(self.save_summary_plots)
        self.pushButton_make_toolpath_plots.clicked.connect(self.make_toolpath_plots)
        self.page2_pushbutton_save_toolpath_plots.clicked.connect(self.save_toolpath_plots)
        # change page to the value stored in the combo box
        self.combo_box_select_page.currentIndexChanged.connect(
            self.stackedWidget.setCurrentIndex
        )
        # reload if preprocess status changed
        self.preprocess_file_checkbox.stateChanged.connect(self.reload_file)

        # Default stacked: zero page
        self.stackedWidget.setCurrentIndex(0)
        # Arbitrary plotting buttons etc
        self.page3_pushbutton_repopulate.clicked.connect(self.populate_arb_var_combo_boxes)
        self.page3_pushbutton_makeplots.clicked.connect(self.make_arb_var_plots)
        self.page3_pushbutton_save_arb_var_plot.clicked.connect(self.save_arb_var_plot)
        # 3D plot button
        # initially grey out laser on, because processing required
        self.page4_checkBox_laseron.setEnabled(False)
        self.preprocess_file_checkbox.toggled.connect(
            self.page4_checkBox_laseron.setEnabled
        ) # enabled 'laser on' plotting when preprocessing
        self.preprocess_file_checkbox.toggled.connect(
            lambda checked: not checked and self.page4_checkBox_laseron.setChecked(False) and self.page4_checkBox_laseron.setEnabled(False) # disable 'laser on' when not preprocessing
        )
        self.page4_checkBox_laseron.stateChanged.connect(
            lambda: self.make_3d_plot(self.page4_column)
        ) # refresh 3D plot when laser status changed
        # set up ordinary plot buttons
        self.page4_pushButton_glassTemp.clicked.connect(lambda: self.make_3d_plot("protectionGlasTemperature"))
        self.page4_pushButton_poolTemp.clicked.connect(lambda: self.make_3d_plot("meltpoolTemp"))
        self.page4_pushButton_poolSize.clicked.connect(lambda: self.make_3d_plot("meltpoolSize"))
        self.page4_pushButton_flowWatch.clicked.connect(lambda: self.make_3d_plot("flowWatch"))
        self.page4_pushButton_Q.clicked.connect(lambda: self.make_3d_plot("t2"))


        # Parse command line. TBD whether there's a better way to mix stock python and Qt
        parser = argparse.ArgumentParser()
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
            # Set preprocessing checkbox on
            self.preprocess_file_checkbox.setChecked(True)
        else:
            self.log_data_df = None


        self.setup_plot_areas()

        

        # Set up the single toolpath plot page
        # There are several ways to do this, but I'm not sure how to use the promote to one,
        # so I'm doing the more obvious way here
        # TODO: Find out how to do using 'promote to' in QT Designer, that should make this
        # section not required
        single_toolpath_plots_form_widget = SingleToolpathPlotsForm(
            self.single_toolpath_page_element
        )
        # TODO: Terrible hack, connect this better with signals/slots/whatever
        # Or use a singleton for data
        single_toolpath_plots_form_widget.link_to_main = self
        self.gridLayout_9.addWidget(single_toolpath_plots_form_widget)


    def setup_plot_areas(self):
        """
        Catch all function to set up all the plot areas

        It would be nice to do this in a more elegant way
        """

        # Create a default plot
        self.plot_fig_1, self.ax1 = plt.subplots(tight_layout=True)
        self.plot_widget_1 = FigureCanvas(self.plot_fig_1)

        # Here turn each of the QWidget plot areas we created into the designer into a layout, and
        # First 3 layouts are the three timeseries plots on page 1
        # This is the line that links handwritten code to the QtDesigner code (widget_PlotArea_1
        # is from the designer)
        p1topright = QtWidgets.QVBoxLayout(self.page1_topright)
        p1topright.setContentsMargins(0, 0, 0, 0)
        p1topright.addWidget(self.plot_widget_1)

        # Create a default plot
        self.plot_fig_2, self.ax2 = plt.subplots(tight_layout=True)
        self.plot_widget_2 = FigureCanvas(self.plot_fig_2)


        p1bottomright = QtWidgets.QVBoxLayout(self.page1_bottomright)
        p1bottomright.setContentsMargins(0, 0, 0, 0)
        p1bottomright.addWidget(self.plot_widget_2)

        # Create a default plot
        self.plot_fig_3, self.ax3 = plt.subplots(tight_layout=True)
        self.plot_widget_3 = FigureCanvas(self.plot_fig_3)


        p1bottomleft = QtWidgets.QVBoxLayout(self.page1_bottomleft)
        p1bottomleft.setContentsMargins(0, 0, 0, 0)
        p1bottomleft.addWidget(self.plot_widget_3)

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
        grid_3d_plot = gl.GLGridItem()
        grid_3d_plot.setSize(200,200)
        grid_3d_plot.setSpacing(5,5)
        self.viewer.addItem(grid_3d_plot)
        return

    def make_3d_plot(self, column, alpha=0.5):
        """
        Generate interactive 3D plot
        TODO: add color bar. This is a little tricky and will require replacing the central
        page 4 widget with an umbrella widget that can contain the 3D plot and 2D colorbar.
        See https://groups.google.com/g/pyqtgraph/c/PfJvmjIF3Dg/m/QVG9xUGk-zgJ
        """
        # save new desired column
        self.page4_column = column
        # clear gl of preexisting scatter
        if self.current_scatter: # remove any preexisting scatter
            self.viewer.removeItem(self.current_scatter)
        # load data, removing laser off sections if desired
        if self.log_data_df is None:
            print("Log Data df empty")
            return
        this_df = self.log_data_df
        if bool(self.page4_checkBox_laseron.checkState()):
            this_df = this_df[
                this_df["laser_on_time(ms)"] > 200
            ]
        else:
            pass

        coords, vals = self.three_d_plot_vals(this_df, self.page4_column)
        cols = cm.plasma(vals) # using the 'plasma' colormap
        cols = to_rgba_array(cols, alpha)
        scatter=gl.GLScatterPlotItem(pos=coords, color=cols, size=3)
        scatter.setGLOptions('opaque')
        self.viewer.addItem(scatter)

        self.current_scatter=scatter # save current scatter
        return

    def three_d_plot_vals(self, input_df, column, use_part_frame=False):
        """
        Generates coordinates and colours for gl scatterplot from dataframe
        """
        # get spatial coords
        # only part frame coordinates if possible
        if bool(self.plot_laser_on.checkState()) and use_part_frame:
            print("inside partFrame loop")
            coords=input_df[['xpart','ypart','zpart']].to_numpy()
        else:
            coords=input_df[['x','y','z']].to_numpy()
        # translate so median values are at origin, for ease of viewing
        coords = coords - np.median(coords, axis=0, keepdims=True)

        # TODO check columnname is valid
        # now colours. These need to be converted to (N,4) RGBA array
        vals = input_df[column].to_numpy() # extract values
        # normalise values to [0,1]
        if np.unique(vals).shape[0]==1: # if constant
            pass
        else:
            # -min moves lowest val to 0, division by range sets range to 1
            vals=(vals-np.min(vals))/np.ptp(vals)
        # then convert to colors using a colormap
        return coords, vals

    def save_arb_var_plot(self):
        """
        When triggered, opens a modal dialog and saves the currently rendered arb var plot

        """
        file_path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self, # Parent
            "Save File", # Title of dialog
            filter="PNG (*.png);;PDF (*.pdf);;SVG (*.svg)"
        )
        # If cancelled
        if file_path == '':
            return
        # Now save plot as currently rendered

        self.arb_var_plotting_objects[0].savefig(file_path)
        return



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

        # Get thresholds from sliders
        # Sliders are on scale of 0 to 100, so do in terms of min and max
        # Could work on percentiles as well, but would like to discuss that first
        x_min_thresh_idx = self.horizontal_slider_arb_var_x_min_thresh.value()
        x_max_thresh_idx = self.horizontal_slider_arb_var_x_max_thresh.value()
        y_min_thresh_idx = self.horizontal_slider_arb_var_y_min_thresh.value()
        y_max_thresh_idx = self.horizontal_slider_arb_var_y_max_thresh.value()
        x_delta = np.max(plot_subset[x_col]) - np.min(plot_subset[x_col])
        y_delta = np.max(plot_subset[y_col]) - np.min(plot_subset[y_col])
        x_min = np.min(plot_subset[x_col]) + x_min_thresh_idx/99 * x_delta
        x_max = np.min(plot_subset[x_col]) + x_max_thresh_idx/99 * x_delta
        y_min = np.min(plot_subset[y_col]) + y_min_thresh_idx/99 * y_delta
        y_max = np.min(plot_subset[y_col]) + y_max_thresh_idx/99 * y_delta
        plot_subset = plot_subset[
            (plot_subset[x_col] >= x_min)
            & (plot_subset[x_col] <= x_max)
            & (plot_subset[y_col] >= y_min)
            & (plot_subset[y_col] <= y_max)
        ]

        ax = self.arb_var_plotting_objects[1]
        ax.cla()
        ax.plot(plot_subset[x_col], plot_subset[y_col])
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        # Draw on the thresholds
        ax.axvline(x_min, label="X min", linestyle="--", color="#648FFF")
        ax.axvline(x_max, label="X max", linestyle="--", color="#785EF0")
        ax.axhline(y_min, label="Y min", linestyle="--", color="#DC267F")
        ax.axhline(y_max, label="Y max", linestyle="--", color="#FE6100")
        ax.set_title("{} vs {}".format(x_col, y_col))
        self.arb_var_plotting_objects[0].legend()
        self.arb_var_plotting_objects[2].draw()
        return

    def save_toolpath_plots(self):
        """
        Saves toolpath plots as currently rendered
        """
        save_folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')
        # Returns None or path
        if save_folder_path is None or save_folder_path == '':
            return
        figs = [
            self.toolpath_plots_dict["poolsize_per_toolpath"][0],
            self.toolpath_plots_dict["pooltemp_per_toolpath"][0],
            self.toolpath_plots_dict["flowwatch_per_toolpath"][0],
        ]
        # Could also use names to address figs above, but not sure about that coupling
        names = [
            "poolsize_per_toolpath",
            "pooltemp_per_toolpath",
            "flowwatch_per_toolpath",
        ]
        for name, fig in zip(names, figs):
            for extension in [".png", ".pdf", ".svg"]:
                save_path = os.path.join(save_folder_path, name + extension)
                fig.savefig(save_path)
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


    def save_summary_plots(self):
        """
        Callback func to save the summary plots as rendered
        Saves all into a folder
        """
        save_folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')
        # Returns None or path
        if save_folder_path is None or save_folder_path == '':
            return
        figs = [self.plot_fig_1, self.plot_fig_2, self.plot_fig_3]
        names = ["meltpool_size", "flow_watch", "protection_glass_temp"]
        for name, fig in zip(names, figs):
            for extension in [".png", ".pdf", ".svg"]:
                save_path = os.path.join(save_folder_path, name + extension)
                fig.savefig(save_path)
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
        # if not preprocessing, we won't have access to t (min) and must plot in milliseconds
        if not bool(self.preprocess_file_checkbox.checkState()):
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
        self.plot_widget_1.draw()

        self.ax2.cla()
        self.ax2.plot(plot_subset[xcolumn], plot_subset["flowWatch"])
        self.ax2.set_xlabel(xlabel)
        self.ax2.set_ylabel("Flow watch sensor (AU)")
        self.ax2.set_title("Flow watch sensor over time")
        # self.plot_fig_2.tight_layout()
        self.plot_widget_2.draw()

        self.ax3.cla()
        self.ax3.plot(plot_subset[xcolumn], plot_subset["protectionGlasTemperature"])
        self.ax3.set_xlabel(xlabel)
        self.ax3.set_ylabel("Protection glass temp (degC)")
        self.ax3.set_title("Protection glass temperature")
        # self.plot_fig_3.tight_layout()
        self.plot_widget_3.draw()

        return

    def reload_file(self):
        """
        Reloads data, for when preprocess checkbox status changes
        """
        if self.last_file: # if previous file exists
            preprocess = bool(self.preprocess_file_checkbox.checkState())
            self.load_and_proc_file(self.last_file, preprocess)
        # If checkbox is checked then turn on all of the fun laser on plotting options, else turn off
        if self.preprocess_file_checkbox.isChecked():
            self.plot_laser_on.setCheckable(True)
            self.page3_checkbox_laser_on.setCheckable(True)
        else:
            self.plot_laser_on.setCheckable(False)
            self.plot_laser_on.setChecked(False)
            self.page3_checkbox_laser_on.setCheckable(False)
            self.page3_checkbox_laser_on.setChecked(False)

        return

    def load_file(self):
        """
        Used to open up the file selector to find path to data file, and then calls
        load_and_proc_file to load it in
        """
        # Use dir to set default folder
        directory = Path("")
        if self.last_dir: # if previous directory, start from there
            directory = self.last_dir

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", str(directory), "Data file (*.dat)"
        )
        preprocess = bool(self.preprocess_file_checkbox.checkState())

        if file_path: # if file chosen
            print("file_path is {}".format(file_path))
            self.last_dir = Path(file_path).parent
            self.last_file = Path(file_path) # save filepath for reloading
            self.load_and_proc_file(file_path, preprocess)

        return

    def load_and_proc_file(self, file_path, preprocess):
        """
        Given path to data file, loads and optionally preprocesses using methods in
        ngif_romar.tools
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
