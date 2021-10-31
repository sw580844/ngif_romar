"""
SW 2021-09-24

Quick script to get around using pyside6-uic to process UI files

Basically runs that, and then does a find/replace from pyside6 to pyside, use at your own risk etc

Assumes pyside6-uic is installed etc
"""

import tempfile
import shutil
import argparse
import subprocess
import sys
import re
import os

def process_file(ui_file_path, output_file_path):
    """
    
    """
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        pyside6_path = os.path.join(tmp_dir_path, "pyside6_file.py")
        pyside2_path = os.path.join(tmp_dir_path, "pyside2_file.py")

        args = [
            "pyside6-uic.exe",
            ui_file_path,
            "--output", pyside6_path
        ]
        result = subprocess.run(args)
        with open(pyside6_path, 'r') as from_file:
            with open(pyside2_path, 'w') as to_file:
                to_file.writelines(
                    re.sub(r"from PySide6", "from PySide2", line) for line in from_file
                )
        shutil.copy2(pyside2_path, output_file_path)

    


    return result

def main():
    """
    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("ui_file_path", help="Path to ui file to process")
    parser.add_argument("output_file_path", help="Output file path")

    args = parser.parse_args()
    process_file(args.ui_file_path, args.output_file_path)

    sys.exit(0)




if __name__ == "__main__":
    main()