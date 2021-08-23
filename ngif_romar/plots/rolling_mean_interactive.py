"""
SW 2021-07-31

Quick implementation of matplotlib interactive plot with rolling mean on meltpool size
"""

import sys
import argparse

import plots_tools

def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_logfile", help="Path to machine logfile")
    parser.add_argument("--process", help="Whether to preprocess data etc", action="store_true")
    parser.add_argument("--log_slider",
        help="Whether interactive slider should be logarithmic", action="store_true"
    )

    args = parser.parse_args()

    _, logfile_df = plots_tools.read_data(args.path_to_logfile)

    plots_tools.show_rolling_mean_meltpool_size(logfile_df, args.process, args.log_slider)


    sys.exit(0)

if __name__ == "__main__":
    main()
