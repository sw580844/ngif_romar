"""
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
    frame_names = [i for i in os.listdir(input_folder) if i[-4:] == ".dat"]
    frame_names = sorted(frame_names)

    print("Max frames is {}".format(max_frames))
    if len(frame_names) == 0:
        print("No .dat frames found, movie will not be created")
        return 2
    # Open first frame to work out the size etc
    frame = read_and_convert_image(os.path.join(input_folder, frame_names[0]))
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
        frame = np.genfromtxt(os.path.join(
                input_folder,
                frame_name,
            ),
            dtype=int
        )
        frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        if scale_x or scale_y:
            frame = resize_image(frame, scale_x, scale_y)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
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
    parser.add_argument("frame_folder_path", help="Path to folder containing .dat images")
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

    print("Packing frames in folder {} into movie {} with FPS {}".format(
        args.frame_folder_path, args.output_filepath, args.fps))
    if args.max_frames:
        print("Limited to first {} frames".format(args.max_frames))

    if not os.path.isdir(args.frame_folder_path):
        print("Path {} is not a folder, quitting early".format(args.frame_folder_path))
        sys.exit(1)

    pack_files_return_value = pack_files(input_folder=args.frame_folder_path,
               output_filepath=args.output_filepath,
               fps=args.fps,
               max_frames=args.max_frames,
               scale_x=args.scale_x, scale_y=args.scale_y,
    )

    sys.exit(pack_files_return_value)


if __name__ == "__main__":
    main()
