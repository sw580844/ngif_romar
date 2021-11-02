"""
SW 2021-11-02

Quick UI to do the frame packer stuff
"""
import os
import sys

from PyQt5 import QtWidgets

from frame_packer_ui import Ui_MainWindow
try:
    from ngif_romar import tools
    from ngif_romar import frames_to_movie
except ModuleNotFoundError as error:
    # If not in path/installed, use relative import
    module_path = os.path.abspath(os.path.join(".."))
    sys.path.append(module_path)
    from ngif_romar import tools
    from ngif_romar.frames_to_movie import frames_to_movie

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main window of POC app
    """
    def __init__(self):
        # super(MainWindow, self).__init__()
        super().__init__()
        self.setupUi(self)


        self.output_path = None
        self.input_folder_path = None

        # Set up callbacks
        self.push_button_open_folder.clicked.connect(self.load_folder)
        self.last_dir = None # last visited directory, for reference when loading files
        self.push_button_select_output_path.clicked.connect(self.select_output_path)
        self.push_button_pack_files.clicked.connect(self.pack_files)



    def pack_files(self):
        """
        TODO: Break into threads, progress bar, etc
        """
        print("Start pack")
        # Check inputs, outputs set, then run other code
        if self.output_path is None or self.input_folder_path is None:
            self.label_pack_status.setText("Output path or input path missing")
            self.label_pack_status.adjustSize()
            return

        self.label_pack_status.setText("Started packing")
        self.label_pack_status.adjustSize()
        frames_to_movie.pack_files(self.input_folder_path, self.output_path, 60)

        self.label_pack_status.setText("Finished packing")
        self.label_pack_status.adjustSize()
        return


    def select_output_path(self):
        """

        """
        print("Select outout?")
        result = QtWidgets.QFileDialog.getSaveFileName(
            self, # Parent
            "Save File", # Title of dialog
            filter="Video (*.mp4)"
        )
        # If cancelled
        if result[0] == '':
            return

        self.label_output_path.setText(result[0])
        self.label_output_path.adjustSize()
        self.output_path = result[0]


        return



    def load_folder(self):
        """
        Loads in frame folder
        """

        result = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')
        # Returns None or path
        if result is None or result == '':
            return
        self.label_selected_path.setText(result)
        self.label_selected_path.adjustSize()

        # Check folder is composed of .dat files
        files = os.listdir(result)
        dat_files = [i for i in files if i[-4:] == ".dat"]
        self.label_folder_stats.setText(
            "{} .dat files, {} total contents".format(len(dat_files), len(files) - len(dat_files))
        )
        self.label_folder_stats.adjustSize()
        self.input_folder_path = result
        return



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
