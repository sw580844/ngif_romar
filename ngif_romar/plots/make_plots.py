"""
SW 2021-07-31

Generate requested plots from data.dat log file
"""

import sys
import argparse

import plots_tools


def make_plots(log_file_path, output_folder_path, show_plots, pre_process,
    with_and_without_preprocess):
    """
    Function to take in data file, generate plots
    """

    _, log_df = plots_tools.read_data(log_file_path)

    # First plot: meltpool size over time
    plots_tools.make_plot_pool_size_over_time(log_df,
        output_folder_path, show_plot=show_plots, pre_process=pre_process,
        with_and_without_preprocess=with_and_without_preprocess
    )
    plots_tools.make_plot_powder_flow_over_time(log_df,
        output_folder_path, show_plot=show_plots, pre_process=pre_process,
        with_and_without_preprocess=with_and_without_preprocess
    )
    plots_tools.make_plot_protection_glass_temp(log_df,
        output_folder_path, show_plot=show_plots, pre_process=pre_process,
        with_and_without_preprocess=with_and_without_preprocess
    )

    return


def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_logfile", help="Path to machine logfile")
    parser.add_argument("--plots_folder_path",
        help="Path to folder to save plots"
    )
    parser.add_argument(
        "--show_plots", help="Whether to show plots in matplotlib viewer", action="store_true"
    )
    parser.add_argument(
        "--pre_process",
        help="Whether to preprocess data by looking only when laser is on, or including rolling means",
        action="store_true"
    )
    parser.add_argument("--with_and_without_preprocess",
        help="Shows plots with and without preprocessing", action="store_true"
    )

    args = parser.parse_args()

    make_plots(args.path_to_logfile, args.plots_folder_path,
        args.show_plots, args.pre_process, args.with_and_without_preprocess
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
