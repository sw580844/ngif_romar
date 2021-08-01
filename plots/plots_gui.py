"""
SW 2021-08-01

Quickly testing a quick GUI for throwing together plots

See:
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
https://docs.python.org/3/library/tkinter.html
"""

import sys
import tkinter as tk
from tkinter import ttk


from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, )

import plots_tools

# For quickly prototyping



class Application(tk.Frame):
    """
    Basic class representing whole application
    """
    def __init__(self, master=None):
        """
        Constructor
        """
        super().__init__(master)
        self.master = master
        # self.pack()
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """
        Quick func to create all widgets present
        """

        self.control_frame = tk.Frame()
        # No idea why we need to create separate variables for buttons but still
        self.preprocess_value = tk.IntVar()
        self.preprocess_check_button = ttk.Checkbutton(self.control_frame,
            text="Preprocess DF", variable=self.preprocess_value
        )
        self.preprocess_value.set('0')
        # self.preprocess_check_button.pack(side="top")
        self.preprocess_check_button.grid(row=0, column=0, sticky="W")

        self.open_file_button = tk.Button(self.control_frame)
        self.open_file_button["text"] = "Open machine logfile"
        self.open_file_button["command"] = self.browse_and_get_logfile
        # self.open_file_button.pack(side="top")
        self.open_file_button.grid(row=0, column=1, sticky="W")

        self.quit = tk.Button(self.control_frame, text="QUIT", fg="red",
                              command=self.master.destroy)
        # self.quit.pack(side="bottom")
        self.quit.grid(row=0, column=2)

        self.control_frame.grid(row=0,column=0)

        # For clearing later
        self.canvas_pool_size = None
        self.canvas_powder_flow = None
        self.canvas_glass_temp = None





    def browse_and_get_logfile(self):
        """
        Uses filedialog to get path to logfile, then plots etc
        """
        filename = tk.filedialog.askopenfilename()
        print("Filename: {}".format(filename))
        _, self.logfile_df = plots_tools.read_data(filename)


        # Clear previous:
        if self.canvas_pool_size:
            print("Close pool size")
            self.canvas_pool_size.get_tk_widget().destroy()
        if self.canvas_powder_flow:
            print("Close powder flow")
            self.canvas_powder_flow.get_tk_widget().destroy()
        if self.canvas_glass_temp:
            print("Close glass temp")
            self.canvas_glass_temp.get_tk_widget().destroy()

        # TODO: change plotting function to work on axes instead of fig? Or update as necessary
        # blank plots etc

        preprocess_plots = "selected" in self.preprocess_check_button.state()

        self.pool_size_fig = plots_tools.make_plot_pool_size_over_time(
            self.logfile_df, show_plot=False, pre_process=preprocess_plots
        )
        self.canvas_pool_size = FigureCanvasTkAgg(self.pool_size_fig, master=self.master)
        # self.canvas_pool_size.get_tk_widget().pack(side="left")
        self.canvas_pool_size.get_tk_widget().grid(row=0, column=1)

        self.powder_flow_fig = plots_tools.make_plot_powder_flow_over_time(
            self.logfile_df, show_plot=False, pre_process=preprocess_plots
        )
        self.canvas_powder_flow = FigureCanvasTkAgg(self.powder_flow_fig, master=self.master)
        # self.canvas_powder_flow.get_tk_widget().pack(side="left")
        self.canvas_powder_flow.get_tk_widget().grid(row=1, column=0)

        self.glass_temp_fig = plots_tools.make_plot_protection_glass_temp(
            self.logfile_df, show_plot=False, pre_process=preprocess_plots
        )
        self.canvas_glass_temp = FigureCanvasTkAgg(self.glass_temp_fig, master=self.master)
        # self.canvas_glass_temp.get_tk_widget().pack(side="left")
        self.canvas_glass_temp.get_tk_widget().grid(row=1, column=1)



    



def main():
    """
    Main entry point, starts up TK mainloop
    """
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    sys.exit(0)

if __name__ == "__main__":
    main()
