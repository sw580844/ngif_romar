# GUI for summarising print job
# Input: Data.dat file
# Output: Pane with 3D plot of path on lhs, and timeseries plots of key variables on rhs
# Stretch goal: synchronised animation: vertical line moving over the plots, with 3D animation showing location on the left
# Stre-etch: in the future we could follow up the animation with a summary of statistics/more tools

# Based off of https://www.journaldev.com/48165/tkinter-working-with-classes

import tkinter as tk
from tkinter import ttk # for themed widgets
from tkinter import filedialog as fd # for handling files
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

import os
def readData(target): # Load Data.dat files into dataframes
    prevdir = os.getcwd()
    df = pd.read_csv(target, sep=" ", comment='#')
    df = df[df['LaserPower']>0] # trim where laser is off
    os.chdir(prevdir)
    return df

# class WrappingLabel by "rmb" on stackexchange
class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

class window(tk.Tk): # root-level window
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) # initialise a Tk
        self.wm_title("Data visualiser") # add title to the window
        # set up container (a frame) within the window where different frames will appear
        container = tk.Frame(self, height=400,width=600)
        container.pack(side="top",fill="both",expand=True) # region within window
        container.grid_rowconfigure(0, weight=1) # row 0, resizeable
        container.grid_columnconfigure(0, weight=1)

        # shared data
        self.shared_data = {
            "fn": str, # filename
            "df": pd.core.frame.DataFrame # dataframe
        }

        # dictionary of frames to be switched between
        self.frames = {}
        # frames will be created later, but we'll add components to the dict here
        for F in (LoadPage, poolSizePage):#, poolTempPage, flowWatchPage, glasTempPage):
            frame = F(container, self)
            self.frames[F] = frame # window class acts as root window for the frames
            frame.grid(row=0,column=0, sticky="nswew") # all frames centered in root window

        self.show_frame(LoadPage) # initialise on LoadPage

        
    # end init
    def show_frame(self, cont):
        frame = self.frames[cont] # select the chosen frame from the dictionary
        frame.tkraise() # raise that frame to the top

class LoadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # initialise frame
        # allow resizing
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        # label describing opened file
        labeltextVar = tk.StringVar(self)
        labeltextVar.set("No file chosen.")
        fileinfoText = WrappingLabel(self, textvar=labeltextVar, height=12)
        fileinfoText.grid(column=0,row=0,sticky='nsew') # position text

        # file opener
        def file_opener():
            filetypes = (
                ('Data files', '*.dat'),
                ('All files', '*.*')
            )
            # show browse file dialog
            filename = fd.askopenfilename(filetypes=filetypes)
            labeltextVar.set(filename) # change display text to filename
            # save name and data to shared
            controller.shared_data["fn"] = filename # save filename to shared
            controller.shared_data["df"] = readData(filename) # load and save dataframe
        
        # open file button
        open_button = ttk.Button(
            self,
            text='Open a File',
            command=file_opener
            )
        open_button.grid(column=0, row=1, sticky='nesw', padx=10, pady=10)

        # page navigation menu
        optionlist = ["Configuration", "poolSize", "poolTemp", "flowWatch", "glasTemp"]
        pagedict = { # drop down menu options -> page classes
            "Configuration" : LoadPage,#
            "poolSize" : poolSizePage,
            "poolTemp" : LoadPage,#poolTempPage,
            "flowWatch": LoadPage,#flowWatchPage,
            "glasTemp" : LoadPage,#glasTempPage
            }
        
        variable = tk.StringVar(self)
        variable.set("Configuration") # initial value
        dropdown = tk.OptionMenu(self, variable,*optionlist)
        dropdown.grid(column=0,row=2,sticky='nsew') # position on bottom
        
        def callback(*args): # make drop down click do something
            controller.show_frame(pagedict[variable.get()]) # converts strings to class names, for dictionary
        variable.trace("w", callback) # track drop down menu button          

class poolSizePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # initialise frame
        # allow resizing
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        # plots (one figure w/ (1,2) subplots)
        

        # page navigation menu
        optionlist = ["Configuration", "poolSize", "poolTemp", "flowWatch", "glasTemp"]
        variable = tk.StringVar(self)
        variable.set("poolSize") # this page is poolSizePage
        dropdown = tk.OptionMenu(self, variable,*optionlist)
        dropdown.grid(column=0,row=1,sticky='nsew') # position on bottom
        pagedict = { # drop down menu options -> page classes
            "Configuration" : LoadPage,#
            "poolSize" : poolSizePage,
            "poolTemp" : LoadPage,#poolTempPage,
            "flowWatch": LoadPage,#flowWatchPage,
            "glasTemp" : LoadPage,#glasTempPage
            }
        
        def callback(*args): # make drop down click do something
            controller.show_frame(pagedict[variable.get()]) # converts strings to class names, for dictionary
        variable.trace("w", callback) # track drop down menu button          


if __name__ == "__main__":
    testObj = window()
    testObj.mainloop()