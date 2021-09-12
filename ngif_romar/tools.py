"""
tools :

Here's the general module/script where we'll put all of the general data preprocessing and other
tools as req

Organisation could change from this script to another subfolder

SW 2021-08-30 - Creation, initial commit
"""

import re
import datetime
import os

import pandas as pd
import numpy as np
import cv2

def read_data(data_path):
    """
    Reads in data from a log file, seperating out the metadata header and the space delimited
    values that follow

    Performs minimal postprocessing, see other funcs for that

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


    return meta_data_dict, data_df

def post_process_log_data(data_df):
    """
    Function to add in supplementary data to the logfile df

    The aim of this function is to add derived data that only relies on this df, other functions
    with add in other relations (such as linking to images present)

    Cylindrical coords will be defined on (-pi to +pi)

    TODO: Too many statements according to pylint

    Args:
        - data_df : Pandas dataframe of logfile data, usually produced from read_data
    """

    # Extra time data
    data_df["t(s)"] = data_df["t"] * 1e-3
    data_df["t(min)"] = data_df["t(s)"] / 60
    # Construct euclidean velocities
    data_df["v_x(mm/ms)"] = np.gradient(data_df["x"], data_df["t"])
    data_df["v_y(mm/ms)"] = np.gradient(data_df["y"], data_df["t"])
    data_df["v_z(mm/ms)"] = np.gradient(data_df["z"], data_df["t"])
    data_df["|v|(mm/ms)"] = np.linalg.norm(
        data_df[["v_x(mm/ms)", "v_y(mm/ms)", "v_z(mm/ms)"]].values,
        axis=1
    )

    # Add in cylindrical coordinate values. Wrap on -pi to +pi, note that there will be jumps
    data_df["phi(rad)"] = np.arctan2(data_df["y"], data_df["x"])
    data_df["r(mm)"] = np.linalg.norm(data_df[["x", "y"]].values, axis=1)

    # For the deriv we'll manually wrap
    # Due to wrapped angle domain we have discontinuities when evaluating angular vel, so we'll
    # need to play carefully with that
    def ang_vel_calc(xs, ys, ts):
        """
        Given xs, ys, and ts this function attempts to deduce the time derivative of the phi
        coordinate in a cylindrical coordinate system

        As arctan2 reports on a range of -pi to +pi, this can lead to discontinous values when
        crossing the crossover point

        For each successive phi_n, phi_{n+1} we calculate the angle difference, and optionally add
        or subtract 2 pi to find the smallest absolute difference.
        For exterior points we calculate the derivative using two points, for interior points we
        use three points

        TODO: I'm sure there's a clearer way to lay out this modular arithmetic

        Args:
            - xs
            - ys
            - ts
        """
        phis = np.arctan2(ys, xs)
        derivs = np.zeros_like(phis)

        # Do first, last derivs separately
        # Modular arithmetic in 2pi

        # Find angle diff between different rows, with optional 2pi due to modular arithmetic
        angle_diffs = [
            abs(phis[1] - phis[0]),
            abs(phis[1] - phis[0] - 2*np.pi),
            abs(phis[1] - phis[0] + 2*np.pi)
        ]
        # Choose the smallest absolute value
        if np.argmin(angle_diffs) == 0:
            angle_diff = phis[1] - phis[0]
        elif np.argmin(angle_diffs) == 1:
            angle_diff = phis[1] - phis[0] - 2*np.pi
        else:
            angle_diff = phis[1] - phis[0] + 2*np.pi
        # Normal dx/dt derivative
        derivs[0] = angle_diff / (ts[1] - ts[0])

        # Similar process for end exterior point
        angle_diffs = [
            abs(phis[-1] - phis[-2]),
            abs(phis[-1] - phis[-2] - 2*np.pi),
            abs(phis[-1] - phis[-2] + 2*np.pi)
        ]
        if np.argmin(angle_diffs) == 0:
            angle_diff = phis[-1] - phis[-2]
        elif np.argmin(angle_diffs) == 1:
            angle_diff = phis[-1] - phis[-2] - 2*np.pi
        else:
            angle_diff = phis[-1] - phis[-2] + 2*np.pi
        derivs[-1] = angle_diff / (ts[-1] - ts[-2])

        # Now iterate over all internal points
        for i in range(1, len(derivs)-1):
            # Calculate forward derivative in modular arithmetic
            angle_diffs = [
                abs(phis[i+1] - phis[i+0]),
                abs(phis[i+1] - phis[i+0] - 2*np.pi),
                abs(phis[i+1] - phis[i+0] + 2*np.pi)
            ]
            if np.argmin(angle_diffs) == 0:
                angle_diff = phis[i+1] - phis[i+0]
            elif np.argmin(angle_diffs) == 1:
                angle_diff = phis[i+1] - phis[i+0] - 2*np.pi
            else:
                angle_diff = phis[i+1] - phis[i+0] + 2*np.pi
            forward = (angle_diff) / (ts[i+1] - ts[i])

            # Calculate backward derivative in modular arithmetic
            angle_diffs = [
                abs(phis[i] - phis[i-1]),
                abs(phis[i] - phis[i-1] - 2*np.pi),
                abs(phis[i] - phis[i-1] + 2*np.pi)
            ]
            if np.argmin(angle_diffs) == 0:
                angle_diff = phis[i] - phis[i-1]
            elif np.argmin(angle_diffs) == 1:
                angle_diff = phis[i] - phis[i-1] - 2*np.pi
            else:
                angle_diff = phis[i] - phis[i-1] + 2*np.pi
            backward = (angle_diff) / (ts[i] - ts[i-1])
            # Return average of two
            derivs[i] = 0.5 * (forward + backward)

        return derivs
    data_df["phi_dot(rad/ms)"] = ang_vel_calc(
        data_df["x"].values, data_df["y"].values, data_df["t"].values
    )


    def time_since_nonzero(ts, values):
        """
        Quick func to add a new column; time since value was greater than zero

        Used to keep values where the laser has been on for a while

        TODO: test alternative
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.GroupBy.cumcount.html

        """
        result = np.zeros_like(ts)
        idx_last_zero = 0
        for i in range(0, len(ts)):
            if values[i] == 0:
                idx_last_zero = i
                result[i] = 0
            else:
                result[i] = ts[i] - ts[idx_last_zero]
        return result
    data_df["laser_on_time(ms)"] = time_since_nonzero(data_df["t"], data_df["LaserPower"])

    # TODO: Basically above, find a way to put together properly
    # Needed so we can separate some of the frames better, ie. those where the capture is
    # definitely after laser on or off
    def time_since_zero(ts, values):
        """
        Quick func to add a new column; time the column has been zero

        Used to keep values where the laser has been off for a while

        """
        result = np.zeros_like(ts)
        idx_last_nonzero = 0
        for i in range(0, len(ts)):
            if values[i] != 0:
                idx_last_nonzero = i
                result[i] = 0
            else:
                result[i] = ts[i] - ts[idx_last_nonzero]
        return result
    data_df["laser_off_time(ms)"] = time_since_zero(data_df["t"], data_df["LaserPower"])

    def add_toolpath_key(data_df):
        """
        Adds a key identifying different toolpaths to pandas df

        Assumes "laser_on_time(ms)" column has already been added

        Args:
            - data_df : Pandas dataframe as produced by tools.read_data, with a laser_on_time(ms)
                column

        Returns:
            data_df
        """
        start_new_path = np.zeros(len(data_df))
        # Create a flag array of zero or one used to flag when laser switches off
        start_new_path[np.diff(data_df["laser_on_time(ms)"], prepend=0) < 0] = 1
        # This flag array can be used to designate different regions by cumsum
        toolpath_key = np.cumsum(start_new_path)
        # Set the parts of the toolpath_key array where the laser is off to -1
        toolpath_key[data_df["laser_on_time(ms)"] == 0] = -1
        data_df["toolpath_key"] = toolpath_key
        return data_df

    data_df = add_toolpath_key(data_df)
    # Preprocessing finished
    return data_df

def link_camera_frames_to_df(data_df, frame_folder_path):
    """
    Given a dataframe such as those returned by read_data, and optionally postprocessed by
    post_process_log_data, link camera frames to individual rows based on closest timestamp

    Assumes times are consistent, matched using a regex

    Args:
        - data_df : Pandas dataframe as returned by read_data
        - frame_folder_path : Path to folder where images are contained
    """
    time_regex = re.compile(r"\d{8}_\d{6}__(\d+)\.dat")

    time_values = []
    filenames = sorted(os.listdir(frame_folder_path))
    for filename in filenames:
        match_result = time_regex.match(filename)
        time_value = float(match_result.groups()[0])
        time_values.append(time_value)
    time_values = np.array(time_values)

    # Go through each line of the dataframe, and find the frame filename that best matches the t
    # value
    assoc_frame_names = []
    counter = 0
    for t in data_df["t"].values:
        counter = counter + 1
        matching_name = filenames[np.argmin(np.abs(t - time_values))]
        assoc_frame_names.append(matching_name)

    # TODO: Alternative method would be to keep pointers to values and increment through instead
    # of argminning everything
    data_df["matching_frame_filename"] = assoc_frame_names
    return data_df

def read_and_convert_image(filepath, eight_bit=True):
    """
    Takes path to an ASCII frame file, and reads into Numpy array

    Note that some OpenCV functions only accept 8bit arrays

    Args:
        - filepath: Path to the file, assumes an ASCII grid of pixel values
    """

    frame = np.genfromtxt(filepath, dtype=int)
    if eight_bit:
        # Note: cv2.normalize with NORM_MIN_MAX can be inappropriate here, as it will rescale dim
        # values too high, which affects image comparison
        # Explicitly choose scale factor so 4095, the max, gets mapped to 255
        # https://stackoverflow.com/questions/11337499/how-to-convert-an-image-from-np-uint16-to-np-uint8
        frame = cv2.convertScaleAbs(frame, alpha=255.0 / 4095.0)
    return frame
