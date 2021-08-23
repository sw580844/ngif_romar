"""
SW 2021-07-28

Quick script to go through a frame folder and pack into SQLite database

Stored as as binary inside SQlite 

Mostly just to cut down on space at this point
"""

import os
import argparse
import sqlite3
import sys
import pickle
import bz2

import numpy as np

def get_frame_bytes(frame_path):
    """
    Reads in frame as np array, returns pickle byte stream

    Could be changed to remove numpy dep?
    """
    frame = np.genfromtxt(frame_path, dtype=np.uint16)
    frame_pickle_bytes = pickle.dumps(frame)
    frame_pickle_bytes = bz2.compress(frame_pickle_bytes)
    return frame

def create_db(output_path):
    """
    
    """

    try:
        conn = sqlite3.connect(output_path)
        query = """
        CREATE TABLE frame
        (
            pk_frame_id INTEGER PRIMARY KEY,
            filename STRING,
            frame_pickle_data BLOB
        )
        """
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()

    finally:
        conn.close()


def scrape_folder(folder_path, output_path):
    """
    
    """

    if not os.path.exists(output_path):
        create_db(output_path)


    contents = os.listdir(os.path.join(folder_path))
    dat_files = [i for i in contents if i[-4:] == ".dat"]

    for i, dat_file in enumerate(dat_files):
        print("{} of {}           \r".format(i, len(dat_files)), end='')
        filepath = os.path.join(folder_path, dat_file)
        frame_bytes = get_frame_bytes(filepath)
        try:
            conn = sqlite3.connect(output_path)
            insert_statement = """
            INSERT INTO  frame
            (
                filename,
                frame_pickle_data
            )
            VALUES
            (
                ?,
                ?
            )
            """
            cursor = conn.cursor()
            cursor.execute(insert_statement, [dat_file, frame_bytes])
            conn.commit()

        finally:
            conn.close()
    return

def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("frame_folder_path", help="Path to folder containing frames")
    parser.add_argument("output_db_path", help="Path to sqlite db to put results in")

    args = parser.parse_args()
    scrape_folder(args.frame_folder_path, args.output_db_path)

    sys.exit(0)

if __name__ == "__main__":
    main()