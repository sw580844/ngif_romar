"""
2021-09-24 Quick Pyside/QT POC


"""


import sys
import os
import argparse



from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtWidgets
# from PySide2.QtCore import QFile

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
        # self.log_data_df = None


    def make_plots(self):
        """
        Callback function to make plots, assumes data df has been loaded in but squashes this error
        """
        print("Make plots triggered")
        if self.log_data_df is None:
            print("Log data df empty")
            return

        self.ax1.cla()
        self.ax1.plot(self.log_data_df["t(min)"], self.log_data_df["meltpoolSize"])
        self.ax1.set_xlabel("Time (min)")
        self.ax1.set_ylabel("Meltpool size (pix)")
        self.ax1.set_title("Meltpool size over time")
        # self.plot_fig_1.tight_layout()
        self.plotWidget_1.draw()

        self.ax2.cla()
        self.ax2.plot(self.log_data_df["t(min)"], self.log_data_df["flowWatch"])
        self.ax2.set_xlabel("Time (min)")
        self.ax2.set_ylabel("Flow watch sensor (AU)")
        self.ax2.set_title("Flow watch sensor over time")
        # self.plot_fig_2.tight_layout()
        self.plotWidget_2.draw()

        self.ax3.cla()
        self.ax3.plot(self.log_data_df["t(min)"], self.log_data_df["protectionGlasTemperature"])
        self.ax3.set_xlabel("Time (min)")
        self.ax3.set_ylabel("Protection glass temp (degC)")
        self.ax3.set_title("Protection glass temp over time over time")
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



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
