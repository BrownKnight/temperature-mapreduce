# The hadoop streaming process might output the result into multiple files in an output directory
# This script will take all of these files in a specified directory and process them into two CSV files for
# each location, allowing us to create two separate plots

import sys
import urllib.request
import tempfile
from collections import defaultdict
from os import path, makedirs
import glob
from weather import *

args = sys.argv

# Input Validation - Make sure the script is being run correctly
if len(args) != 3:
    print("This script requires the name of the output and new output directory as the only arguments")
    print("Syntax: python3 process_results.py <path_to_directory> <path_to_new_directory>")
    print("Supports local directories and Google Storage (gs://) paths")
    quit()
# Input Validation - End

directory_path = str(args[1])
output_dir = str(args[2])
temp_dir = None

if directory_path.startswith("gs://"):
    print("Downloading files from Google Storage")
    # Create a temp directory on the machine for downloading to
    temp_dir = tempfile.TemporaryDirectory()
    print("DEBUG: Downloading to ", temp_dir)
    urllib.request.urlretrieve(directory_path, temp_dir)
else:
    print("Using local output directory")
    # Instead of using a temp directory, we can simply use the local directory
    temp_dir = path.abspath(directory_path)

# Get all the files in the directory supplied,
# Use list comprehension to ensure we dont pick up any directories that might be in this directory
files = [file_path for file_path in glob.glob(temp_dir + "/*") if
         path.isfile(file_path) and "_SUCCESS" not in file_path]

output_files = defaultdict(list)
for file_path in files:
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            key, value = line.split("-")
            date, location = key.split(".")

            output_files[location].append("%s-%s" % (date, value))

output_dir = path.abspath(output_dir)
makedirs(output_dir, exist_ok=True)
for location in output_files:
    with open(path.join(output_dir, location + ".csv"), "w+") as file:
        for line in output_files[location]:
            file.write("%s\n" % line)
