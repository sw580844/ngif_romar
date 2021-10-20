"""
2021-09-24 Quick Pyside/QT POC

Also check https://stackoverflow.com/questions/43947318/plotting-matplotlib-figure-inside-qwidget-using-qt-designer-form-and-pyqt5
to make sure the process for taking a blank widget and turning into a matplotlib plot is appropriate

Also page 168/178 of matplotlib for python developers

"""


import sys
import os
import argparse


import pandas as pd
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtWidgets
# from PySide2.QtCore import QFile

# Extra includes so py2exe picks them up, presumably this can be done elsehwere
import cv2
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from ui_main_window import Ui_MainWindow

try:
    from ngif_romar import tools
except ModuleNotFoundError as error:
    # If not in path/installed, use relative import
    module_path = os.path.abspath(os.path.join(".."))
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
        self.combo_box_select_page.currentIndexChanged.connect(
            self.stackedWidget_plots.setCurrentIndex
        )
        # Default stacked: zero page
        self.stackedWidget_plots.setCurrentIndex(0)
        # Arbitrary plotting buttons etc
        self.push_button_populate_arb_var_boxes.clicked.connect(self.populate_arb_var_combo_boxes)
        self.push_button_make_arb_var_plots.clicked.connect(self.make_arb_var_plots)


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

    def setup_plot_areas(self):
        """
        Catch all function to set up all the plot areas

        It would be nice to do this in a more elegant way
        """

        # Create a default plot
        self.plot_fig_1, self.ax1 = plt.subplots(tight_layout=True)
        self.plotWidget_1 = FigureCanvas(self.plot_fig_1)

        # Here turn each of the QWidget plot areas we created into the designer into a layout, and
        # add the plot widgets into it
        lay_1 = QtWidgets.QVBoxLayout(self.widget_PlotArea_1)
        lay_1.setContentsMargins(0, 0, 0, 0)
        lay_1.addWidget(self.plotWidget_1)

        # Create a default plot
        self.plot_fig_2, self.ax2 = plt.subplots(tight_layout=True)
        self.plotWidget_2 = FigureCanvas(self.plot_fig_2)

        # Here turn each of the QWidget plot areas we created into the designer into a layout, and
        # add the plot widgets into it
        lay_2 = QtWidgets.QVBoxLayout(self.widget_PlotArea_2)
        lay_2.setContentsMargins(0, 0, 0, 0)
        lay_2.addWidget(self.plotWidget_2)

        # Create a default plot
        self.plot_fig_3, self.ax3 = plt.subplots(tight_layout=True)
        self.plotWidget_3 = FigureCanvas(self.plot_fig_3)

        # Here turn each of the QWidget plot areas we created into the designer into a layout, and
        # add the plot widgets into it
        lay_3 = QtWidgets.QVBoxLayout(self.widget_PlotArea_3)
        lay_3.setContentsMargins(0, 0, 0, 0)
        lay_3.addWidget(self.plotWidget_3)


        # Set up other data?

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

        lay_4 = QtWidgets.QVBoxLayout(self.widget_plot_area_poolsize_per_toolpath)
        lay_4.setContentsMargins(0, 0, 0, 0)
        lay_4.addWidget(self.toolpath_canvas_dict["poolsize_per_toolpath"])

        lay_5 = QtWidgets.QVBoxLayout(self.widget_plot_area_pooltemp_per_toolpath)
        lay_5.setContentsMargins(0, 0, 0, 0)
        lay_5.addWidget(self.toolpath_canvas_dict["pooltemp_per_toolpath"])

        lay_6 = QtWidgets.QVBoxLayout(self.widget_plot_area_flowwatch_per_toolpath)
        lay_6.setContentsMargins(0, 0, 0, 0)
        lay_6.addWidget(self.toolpath_canvas_dict["flowwatch_per_toolpath"])

        # Arbitrary var plotting
        # Objects will be fig, ax, canvas
        self.arb_var_plotting_objects = list(plt.subplots(tight_layout=True))
        self.arb_var_plotting_objects.append(
            FigureCanvas(self.arb_var_plotting_objects[0])
        )
        lay_7 = QtWidgets.QVBoxLayout(self.widget_PlotArea_arb_variable_plotting)
        lay_7.setContentsMargins(0, 0, 0, 0)
        lay_7.addWidget(self.arb_var_plotting_objects[2])




        return

    def make_arb_var_plots(self):
        """
        Generate the arbitrary variable plots
        """
        if self.log_data_df is None:
            print("Log Data df empty")
            return
        plot_subset = self.log_data_df
        if bool(self.check_box_arb_var_plot_only_when_laser_on.checkState()):
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
            plot_subset["t_datetime"] = pd.to_datetime(plot_subset["t(s)"], unit="s")
            # plot_subset = plot_subset.set_index(plot_subset["t_datetime"])
            plot_subset = plot_subset.rolling(
                "{}ms".format(rolling_mean_window), on="t_datetime"
            ).mean()

        self.ax1.cla()
        self.ax1.plot(plot_subset["t(min)"], plot_subset["meltpoolSize"])
        self.ax1.set_xlabel("Time (min)")
        self.ax1.set_ylabel("Meltpool size (pix)")
        self.ax1.set_title("Meltpool size over time")
        # self.plot_fig_1.tight_layout()
        self.plotWidget_1.draw()

        self.ax2.cla()
        self.ax2.plot(plot_subset["t(min)"], plot_subset["flowWatch"])
        self.ax2.set_xlabel("Time (min)")
        self.ax2.set_ylabel("Flow watch sensor (AU)")
        self.ax2.set_title("Flow watch sensor over time")
        # self.plot_fig_2.tight_layout()
        self.plotWidget_2.draw()

        self.ax3.cla()
        self.ax3.plot(plot_subset["t(min)"], plot_subset["protectionGlasTemperature"])
        self.ax3.set_xlabel("Time (min)")
        self.ax3.set_ylabel("Protection glass temp (degC)")
        self.ax3.set_title("Protection glass temperature")
        # self.plot_fig_3.tight_layout()
        self.plotWidget_3.draw()

        return

    def load_file(self):
        """
        Used to open up the file selector to find path to data file, and then calls
        load_and_proc_file to load it in
        """
        # Use dir to set default folder

        file_path, selector_type = QtWidgets.QFileDialog.getOpenFileName(dir=self.default_data_dir)
        preprocess = bool(self.preprocess_file_checkbox.checkState())
        print("file_path is {}".format(file_path))
        # Set default data path to where the file was
        self.default_data_dir = os.path.dirname(file_path)
        print("Set default data dir to {} after file load".format(self.default_data_dir))

        self.load_and_proc_file(file_path, preprocess)

        return

    def load_and_proc_file(self, file_path, preprocess):
        """
        Given path to data file, loads and optionally preprocesses using methods in ngif_romar.tools
        """
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
