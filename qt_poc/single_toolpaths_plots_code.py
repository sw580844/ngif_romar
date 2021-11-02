"""
SW 2021-10-29

This is the .py that sorts out the functionality of the plots of single toolpaths

It imports the .ui/.py single_toolpath_plots_ui.py

It will be imported by main_window_ui.py due to use of the promote to button

"""

import typing


import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets

from single_toolpath_plots_ui import Ui_SingleToolpathPlots

def get_main_window() -> typing.Union[QtWidgets.QMainWindow, None]:
    """
    Quick function to get main window, taken from forum.qt.io
    """
    # Get access to main application
    this_app = QtWidgets.QApplication.instance()
    # Iterate through top level widgets of application to get the main window, which has DF
    print("Top level widgets: {}".format(this_app.topLevelWidgets()))
    for widget in this_app.topLevelWidgets():
        if isinstance(widget, QtWidgets.QMainWindow):
            return widget
    return None


class SingleToolpathPlotsForm(QtWidgets.QWidget, Ui_SingleToolpathPlots):
    """
    Class to represent widget that will hold and deal with all single toolpath plots
    """
    def __init__(self, parent=None ):
        """
        Constructor for the single toolpath plots form

        Inherits from UI, then we set up the other code here. To be inserted into QWidget by main
        window
        """
        # As far as I know, and I need to check, some_arg here is the parent widget
        # And it is, checked here
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(parent)

        super(SingleToolpathPlotsForm, self).__init__(parent)

        self.setup_plot_area()
        # # Set up other callbacks, etc
        self.push_button_repopulate_variables.clicked.connect(self.repopulate_menus)
        self.push_button_make_plots.clicked.connect(self.make_single_toolpath_plots)
        # TODO: decided whether to redraw once slider has finished moving or as is, could be 
        # slow etc
        self.horizontal_slider_select_toolpath.valueChanged.connect(self.on_slider_move)

    def setup_plot_area(self):
        """
        Basically, constructor for plots. Generates matplotlib widgets and inserts into the place
        holder widgets
        """
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


    def on_slider_move(self, slider_val):
        """
        When slider is moved, adjust combo box and redraw plots
        """
        self.make_single_toolpath_plots()
        return


    def repopulate_menus(self):
        """
        Function to repopulate the comobo box for single toolpath plots
        """

        log_data_df = self.link_to_main.log_data_df



        if log_data_df is None:
            print("Log data df empty")
            return
        if "toolpath_key" not in log_data_df.keys():
            print("Toolpath key not present")
            return



        # Reset slider
        self.horizontal_slider_select_toolpath.setRange(
            log_data_df["toolpath_key"].min().astype(int),
            log_data_df["toolpath_key"].max().astype(int),
        )
        print("Repopulated")


        return



    def make_single_toolpath_plots(self,):
        """
        Updates the single toolpath plots
        """

        log_data_df = self.link_to_main.log_data_df

        if log_data_df is None:
            print("Log Data df empty")
            return
        if "toolpath_key" not in log_data_df.keys():
            print("Toolpath key not present")
            return
        # Assume for testing toolpath key is set



        plot_subset = log_data_df[
            (log_data_df["toolpath_key"] == self.horizontal_slider_select_toolpath.value())
            & (log_data_df["laser_on_time(ms)"] > self.spin_box_laser_on_time_thresh.value())
        ]

        self.ax_tr.cla()
        self.ax_tr.plot(plot_subset["t(min)"], plot_subset["flowWatch"])
        self.ax_tr.set_xlabel("t(min)")
        self.ax_tr.set_ylabel("Flow watch sensor\n(au)")
        self.plot_widget_tr.draw()

        self.ax_bl.cla()
        self.ax_bl.plot(plot_subset["t(min)"], plot_subset["meltpoolSize"])
        self.ax_bl.set_xlabel("t(min)")
        self.ax_bl.set_ylabel("Meltpool size\n(pix)")
        self.plot_widget_bl.draw()

        self.ax_br.cla()
        self.ax_br.plot(plot_subset["t(min)"], plot_subset["meltpoolTemp"])
        self.ax_br.set_xlabel("t(min)")
        self.ax_br.set_ylabel("Meltpool temp.\n(degC)")
        self.plot_widget_br.draw()


        return
