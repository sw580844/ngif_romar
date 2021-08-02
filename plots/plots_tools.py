"""
SW 2021-07-31

File for basic data reading, processing, etc
"""
import datetime
import re
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def read_data(data_path):
    """
    Reads in data from a log file, seperating out the metadata header and the space delimited
    values that follow

    Args:
        - data_path: Path to datafile.
    """
    meta_data_lines = []
    with open(data_path, 'r') as a_file:
        for line in a_file:
            # Read the metadata in first, then halt at the empty line where the rest of the data
            # begins
            if line != "\n":
                meta_data_lines.append(line)
            else:
                data_df = pd.read_csv(a_file, header=0, delimiter=' ')

    meta_data_dict = {}
    int_regex = re.compile(r"-?\d+$")
    float_regex = re.compile(r"-?\+?\d+\.?\d*e?\+?-?\d*$")
    meta_data_regex = re.compile(r"# (.*): (.*)\n")
    for line in meta_data_lines:
        match_result = meta_data_regex.match(line)
        key, value = match_result.groups()
        if int_regex.match(value):
            value = int(value)
            continue
        if float_regex.match(value):
            value = float(value)
        meta_data_dict[key] = value
    meta_data_dict["datetime"] = datetime.datetime.strptime(meta_data_dict["Date"], "%Y%m%d_%H%M_")
    data_df["t(s)"] = data_df["t"] * 1e-3
    data_df["t(min)"] = data_df["t(s)"] / 60

    return meta_data_dict, data_df

def show_rolling_mean_meltpool_size(logfile_df, pre_process=False, log_slider=False):
    """
    Makes, shows a meltpool temp plot with rolling mean (and laser thresh I guess)

    See https://matplotlib.org/stable/gallery/widgets/slider_demo.html

    Args:
        - logfile_df: Pandas dataframe of machine log, produced by read_data function
        - process: If true, remove elements of logfile_df where laser is off
        - log_slider: If true, attempts to use a logarithmically varying slider. Doesn't work well
    """


    if pre_process:
        subset = logfile_df[
            logfile_df["LaserPower"] > 0
        ]
    else:
        subset = logfile_df
    fig, axis = plt.subplots()
    axis.plot(logfile_df["t(min)"], logfile_df["meltpoolSize"], label="Data as presented")
    axis.set_xlabel("Time (min)")
    axis.set_ylabel("Meltpool size (pix)")
    window = 0 # Default zero
    line, = axis.plot(subset["t(min)"], subset["meltpoolSize"].rolling(window).mean(),
        label="Rolling mean"
    )

    plt.subplots_adjust(bottom=0.25)
    ax_window = plt.axes([0.25, 0.1, 0.65, 0.03], )
    if log_slider:
        window_slider = Slider(
            ax=ax_window,
            label="Rolling mean window",
            valmin=1,
            valmax=10**10, # Max value ~ 1hr
            valinit=1,
        )
    else:
        window_slider = Slider(
            ax=ax_window,
            label="Rolling mean window",
            valmin=1,
            valmax=500, #
            valinit=1,
        )
    def update(val):
        """
        Function to update plot on slider movement
        """
        if log_slider:
            # https://stackoverflow.com/questions/39960791/logarithmic-slider-with-matplotlib
            new_window = np.log10(window_slider.val)
            window_slider.valtext.set_text(new_window)
        else:
            new_window = window_slider.val
        line.set_ydata(subset["meltpoolSize"].rolling(
            int(new_window),
            center=True,
            min_periods=1,
        ).mean())
        fig.canvas.draw_idle()
        return

    window_slider.on_changed(update)
    fig.legend()
    plt.show()
    return


def make_plot_pool_size_over_time(logfile_df, save_folder_path=None, show_plot=False,
    pre_process=False, with_and_without_preprocess=False):
    """
    Makes a plot using given df of meltpool size over time

    Args:
        - logfile_df: Pandas dataframe of L-DED machine log. Usually gathered by read_data function
        - save_folder_path: Optional, path to folder to save plots
        - show_plot: If True, call plt.show() to show the plots
        - pre_process: If True preprocess the dataframe before plotting. Includes only points
            with laser on and produces extra rolling mean plots
        - with_and_without_preprocess: If True, make plots with and without preprocessing the
            dataframe
    """

    # Basic plot, values as is
    if not pre_process:
        fig, axis = plt.subplots()
        axis.plot(logfile_df["t(min)"], logfile_df["meltpoolSize"])
        axis.set_xlabel("Time (min)")
        axis.set_ylabel("Meltpool size (pix)")
        axis.set_title("Meltpool size over time, data as reported")
        if save_folder_path:
            fig.tight_layout()
            extensions = [".png", ".pdf", ".svg"]
            filename = "meltpool_size_over_time_as_measured"
            for extension in extensions:
                save_path = os.path.join(save_folder_path, filename + extension)
                fig.savefig(save_path)
        if show_plot:
            plt.show()

    if pre_process or with_and_without_preprocess:
        subset = logfile_df[
            logfile_df["LaserPower"] > 0
        ]
        # Weeding out, rolling mean window, etc
        fig, axis = plt.subplots()
        axis.plot(subset["t(min)"], subset["meltpoolSize"], label="As sampled")
        window = 20 # Corresponds to 2s
        axis.plot(subset["t(min)"],
            subset["meltpoolSize"].rolling(window, center=True, min_periods=1).mean(),
            label="Rolling mean window {}s".format(window/10)
        )
        window = 1200 # Corresponds to 2min
        axis.plot(subset["t(min)"],
            subset["meltpoolSize"].rolling(window, center=True, min_periods=1).mean(),
            label="Rolling mean window {}s".format(window/10)
        )
        axis.set_xlabel("Time (min)")
        axis.set_ylabel("Meltpool size (pix)")
        axis.set_title("Meltpool size over time, data processed")
        axis.legend()
        if save_folder_path:
            fig.tight_layout()
            extensions = [".png", ".pdf", ".svg"]
            filename = "meltpool_size_over_time_preprocessed"
            for extension in extensions:
                save_path = os.path.join(save_folder_path, filename + extension)
                fig.savefig(save_path)
        if show_plot:
            plt.show()
    fig.tight_layout()
    return fig

def make_plot_powder_flow_over_time(logfile_df, save_folder_path=None, show_plot=False,
    pre_process=False, with_and_without_preprocess=False):
    """
    Make a plot of the powder flow over time

    Args:
        - logfile_df: Pandas dataframe of L-DED machine log. Usually gathered by read_data function
        - save_folder_path: Optional, path to folder to save plots
        - show_plot: If True, call plt.show() to show the plots
        - pre_process: If True preprocess the dataframe before plotting. Includes only points
            with laser on and produces extra rolling mean plots
        - with_and_without_preprocess: If True, make plots with and without preprocessing the
            dataframe
    """
    if not pre_process:
        fig, axis = plt.subplots()
        axis.plot(logfile_df["t(min)"], logfile_df["flowWatch"])
        axis.set_xlabel("Time (min)")
        axis.set_ylabel("Powder flow watch sensor value")
        axis.set_title("Powder flow over time as measured")
        if save_folder_path:
            fig.tight_layout()
            extensions = [".png", ".pdf", ".svg"]
            filename = "powder_flow_over_time_as_measured"
            for extension in extensions:
                save_path = os.path.join(save_folder_path, filename + extension)
                fig.savefig(save_path)
        if show_plot:
            plt.show()
    if pre_process or with_and_without_preprocess:
        subset = logfile_df[
            logfile_df["LaserPower"] > 0
        ]
        # Weeding out, rolling mean window, etc
        fig, axis = plt.subplots()
        axis.plot(subset["t(min)"], subset["flowWatch"], label="As sampled")
        window = 20 # Corresponds to 2s
        axis.plot(subset["t(min)"],
            subset["flowWatch"].rolling(window, center=True, min_periods=1).mean(),
            label="Rolling mean window {}s".format(window/10)
        )
        window = 1200 # Corresponds to 2min
        axis.plot(subset["t(min)"],
            subset["flowWatch"].rolling(window, center=True, min_periods=1).mean(),
            label="Rolling mean window {}s".format(window/10)
        )
        axis.set_xlabel("Time (min)")
        axis.set_ylabel("Powder flow watch sensor value")
        axis.set_title("Powder flow over time, data preprocessed")
        axis.legend()
        if save_folder_path:
            fig.tight_layout()
            extensions = [".png", ".pdf", ".svg"]
            filename = "powder_flow_over_time_preprocessed"
            for extension in extensions:
                save_path = os.path.join(save_folder_path, filename + extension)
                fig.savefig(save_path)
        if show_plot:
            plt.show()
    fig.tight_layout()
    return fig

def make_plot_protection_glass_temp(logfile_df, save_folder_path=None, show_plot=False,
    pre_process=False, with_and_without_preprocess=False):
    """
    Creates plots of protection glass temperature over time

    Args:
        - logfile_df: Pandas dataframe of L-DED machine log. Usually gathered by read_data function
        - save_folder_path: Optional, path to folder to save plots
        - show_plot: If True, call plt.show() to show the plots
        - pre_process: If True preprocess the dataframe before plotting. Includes only points
            with laser on and produces extra rolling mean plots
        - with_and_without_preprocess: If True, make plots with and without preprocessing the
            dataframe
    """
    if not pre_process:
        fig, axis = plt.subplots()
        axis.plot(logfile_df["t(min)"], logfile_df["protectionGlasTemperature"])
        axis.set_xlabel("Time (min)")
        axis.set_ylabel("Protection glass temperature ($\\degree $C)")
        axis.set_title("Protection glass temperature over time as measured")
        if save_folder_path:
            fig.tight_layout()
            extensions = [".png", ".pdf", ".svg"]
            filename = "protection_glass_temp_over_time_as_measured"
            for extension in extensions:
                save_path = os.path.join(save_folder_path, filename + extension)
                fig.savefig(save_path)
        if show_plot:
            plt.show()
    if pre_process or with_and_without_preprocess:
        subset = logfile_df[
            logfile_df["LaserPower"] > 0
        ]
        # Weeding out, rolling mean window, etc
        fig, axis = plt.subplots()
        axis.plot(subset["t(min)"], subset["protectionGlasTemperature"], label="As sampled")
        window = 20 # Corresponds to 2s
        axis.plot(subset["t(min)"],
            subset["protectionGlasTemperature"].rolling(window, center=True, min_periods=1).mean(),
            label="Rolling mean window {}s".format(window/10)
        )
        window = 1200 # Corresponds to 2min
        axis.plot(subset["t(min)"],
            subset["protectionGlasTemperature"].rolling(window, center=True, min_periods=1).mean(),
            label="Rolling mean window {}s".format(window/10)
        )
        axis.set_xlabel("Time (min)")
        axis.set_ylabel("Protection glass temperature ($\\degree $C)")
        axis.set_title("Protection glass temperature over time, preprocessed")
        axis.legend()

        if save_folder_path:
            fig.tight_layout()
            extensions = [".png", ".pdf", ".svg"]
            filename = "protection_glass_temp_over_time_preprocessed"
            for extension in extensions:
                save_path = os.path.join(save_folder_path, filename + extension)
                fig.savefig(save_path)
        if show_plot:
            plt.show()
    fig.tight_layout()
    return fig
