#!/usr/bin/python3

# The hadoop streaming process will most likely output the result into multiple files (1 for each reducer users)
# in an output directory
# This script will take all of these files in a specified directory and process them into separate CSV files for
# each location, allowing us to create separate plots
# The script is designed to work with any number of locations depending on the input, so minimal/no maintenance will be
# required for this script to use it for other locations

import sys
import tempfile
from collections import defaultdict
from os import makedirs
import glob
from google_storage_helpers import *


def main(args):
    if len(args) != 3:
        print("This script requires the name of the output and new output directory as the only arguments")
        print("Syntax: python3 process_results.py <path_to_directory> <path_to_new_directory>")
        print("Supports local directories and Google Storage (gs://) paths")
        quit()

    arg_directory_path = str(args[1])
    arg_processed_output_dir = str(args[2])

    if arg_directory_path.startswith("gs://"):
        print("Creating temporary dirs and downloading files from Google Storage")

        # Create some temp directories to store the output/processed_output on the machine for downloading/uploading
        temp_dir = tempfile.TemporaryDirectory()
        directory_path = path.abspath(path.join(temp_dir.name, "output"))
        makedirs(directory_path, exist_ok=True)
        processed_output_dir = path.abspath(path.join(temp_dir.name, "processed_output"))
        makedirs(processed_output_dir, exist_ok=True)

        download_from_gs(arg_directory_path, directory_path)
    else:
        print("Using local output directory")
        # Instead of using a temp directory, we can simply use the local directory, and we make sure the processed
        # output directory exists
        directory_path = path.abspath(arg_directory_path)
        processed_output_dir = path.abspath(arg_processed_output_dir)
        makedirs(processed_output_dir, exist_ok=True)

    # Get all the files in the directory supplied,
    # Use list comprehension to ensure we dont pick up any directories that might be in this directory
    files = [file_path for file_path in glob.glob(directory_path + "/*")
             if path.isfile(file_path) and "_SUCCESS" not in file_path]

    print("Processing files")

    processed_output_files = defaultdict(list)
    for file_path in files:
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                key, value = line.split("-")
                date, location = key.split(".")

                # We can filter out any erroneous values here
                if float(value) > 900:
                    print("Found a erroneous value for %s on %s (%s), skipping this value" % (location, date, value))
                else:
                    # If it isn't an erroneous value, then add it to the values to be written to file
                    processed_output_files[location].append("%s-%s" % (date, value))

    for location in processed_output_files:
        with open(path.join(processed_output_dir, location + ".csv"), "w+") as file:
            location_data = []
            # By using copying all the data for each location into an array before writing it to a file, we can sort
            # the array into date-order (which due the the way we format dates, is the same as alphabetical order)
            for line in processed_output_files[location]:
                location_data.append(line)
            location_data.sort()

            for line in location_data:
                file.write(line + "\n")

    print("%s Processed Files have been written to %s" % (len(processed_output_files), processed_output_dir))

    # If using Google Storage, we need to upload the results
    if arg_directory_path.startswith("gs://"):
        print("Uploading results to Google Storage")

        for location in processed_output_files:
            print("Uploading %s result file" % location)
            upload_to_gs(path.join(arg_processed_output_dir, location + ".csv"),
                         path.join(processed_output_dir, location + ".csv"))

        print("Cleaning up temporary directories")
        temp_dir.cleanup()


if __name__ == "__main__":
    main(sys.argv)
