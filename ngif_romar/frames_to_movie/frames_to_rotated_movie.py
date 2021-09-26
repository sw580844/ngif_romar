"""
TH 2021-09-13

Adds on frame rotation

SW 2021-07-25

Quick script to mash together some of the .dat files into a short movie

Assumes the file format corresponds roughly to a date/time

Packs frames into movie by alphabetical filename order
"""

import argparse
import os
import sys
import datetime

import cv2
import numpy as np

try:
    import ngif_romar.tools as tools
except ModuleNotFoundError as error:
    # If not in path/installed, use relative import
    oneback_path = os.path.abspath(os.path.join(".."))
    twoback_path = os.path.abspath(os.path.join("../.."))
    sys.path.append(oneback_path); sys.path.append(twoback_path)
    import ngif_romar.tools as tools

import imutils

def read_and_convert_image(filepath):
    """
    Takes path to an ASCII frame file, and converts to 3 channel BGR for writing to video

    Args:
        - filepath: Path to the file, assumes an ASCII grid of pixel values
    """

    frame = np.genfromtxt(filepath, dtype=int)
    frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    return frame

def resize_image(frame, scale_x=1, scale_y=1):
    """
    Rescale the image

    Args:
        - frame: Frame as numpy array
        - scale_x: Horizontal rescale factor
        - scale_y: Vertical rescale factor
    """
    if scale_x is None:
        scale_x = 1
    if scale_y is None:
        scale_y = 1
    width, height = frame.shape[1], frame.shape[0]
    new_width, new_height = int(scale_x * width), int(scale_y * height)
    frame = cv2.resize(frame,
                       (new_width, new_height),
                       interpolation=cv2.INTER_CUBIC
    )
    return frame

def unique(v):
    unqs = []
    for i in v:
        if i not in unqs:
            unqs.append(i)
    return unqs

def pack_files(input_folder, output_filepath, fps, max_frames=None, scale_x=None, scale_y=None):
    """
    General function call to go through folder of frame files and pack into video

    Args:
        input_folder - Path to folder containing frames
        output_filepath - Path to video to create, should have extension .mp4
        fps - FPS of video to create
        max_frames - Maximum amount of frames in video
        scale_x - To rescale horizontally prior to packing
        scale_y - To rescale vertically prior to packing
    """
    logfile_path = os.path.join(input_folder, "Data.dat")
    frames_path = os.path.join(input_folder, "Frames")
    _, df = tools.read_data(logfile_path)
    df = tools.post_process_log_data(df) # add velocities, among other stuff
    df = tools.link_camera_frames_to_df(df, frames_path) # link to camera frames

    frame_names = [i for i in os.listdir(frames_path) if i[-4:] == ".dat"]
    frame_names = sorted(frame_names) # sort lexicographically -> chronologically
    
    print("Max frames is {}".format(max_frames))
    if len(frame_names) == 0:
        print("No .dat frames found, movie will not be created")
        return 2 

    # Open first frame to work out the size etc
    frame = read_and_convert_image(os.path.join(frames_path, frame_names[0]))
    width, height = frame.shape[1], frame.shape[0]
    if scale_x is None:
        scale_x = 1
    if scale_y is None:
        scale_y = 1
    width, height = int(scale_x * width), int(scale_y * height)

    # Create the writer
    # Just picking the mp4v codec, this could be changed or decided by user
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        output_filepath, # filename
        codec, # codec int code
        fps, # frames per second
        (width, height),
        True, # try color
    )

    if max_frames:
        number_frames = min(len(frame_names), max_frames)
    else:
        number_frames = len(frame_names)

    for i, frame_name in enumerate(frame_names[:number_frames]):
        print("{} of {}               \r".format(i, number_frames), end="")

        # figure out angle to rotate frame by, using velocities of data subset
        subset = df[df['matching_frame_filename']==frame_name]
        avg_vx, avg_vy, avg_vz = np.mean(subset[['v_x(mm/ms)','v_y(mm/ms)','v_z(mm/ms)']])
        angle = np.arctan2(-avg_vx,avg_vy)
        
        frame = tools.read_and_convert_image(os.path.join(frames_path,frame_name,)
            )

        # rotate frame to ^y, >x orientation
        frame = imutils.rotate(frame, angle= -1*angle*180/np.pi)
        # normalise and optionally rescale frame
        frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        if scale_x or scale_y:
            frame = resize_image(frame, scale_x, scale_y)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        # attach time text
        this_datetime = datetime.datetime.strptime(frame_name[:15], "%Y%m%d_%H%M%S",)
        cv2.putText(img=frame,
                    text="{}".format(this_datetime.strftime("%Y-%m-%d %H:%M:%S")),
                    org=(1,20,), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255,0,0) )
        writer.write(frame)
    print("") # Clear buffer from prior status update
    writer.release()

    # No issues, return
    return 0


def main():
    """
    Main entry point
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", help="Path to folder containing Data.dat and /Frames")
    parser.add_argument(
        "output_filepath",
        help="Output path to write movie, should have extension .mp4"
    )
    parser.add_argument("fps", help="FPS of movie", type=float)
    parser.add_argument(
        "--max_frames",
        help="Maximum number of frames to pack into movie", type=int
    )
    parser.add_argument("--scale_x", type=float, help="Rescale the X dimension of the images")
    parser.add_argument("--scale_y", type=float, help="Rescale the Y dimension of the images")
    
    args = parser.parse_args()

    print("Packing frames in folder {}/Frames into movie {} with FPS {}".format(
        args.data_path, args.output_filepath, args.fps))
    if args.max_frames:
        print("Limited to first {} frames".format(args.max_frames))

    if not os.path.isdir(args.data_path):
        print("Path {} is not a folder, quitting early".format(args.data_path))
        sys.exit(1)

    pack_files_return_value = pack_files(input_folder=args.data_path,
               output_filepath=args.output_filepath,
               fps=args.fps,
               max_frames=args.max_frames,
               scale_x=args.scale_x, scale_y=args.scale_y,
    )

    sys.exit(pack_files_return_value)


if __name__ == "__main__":
    main()
