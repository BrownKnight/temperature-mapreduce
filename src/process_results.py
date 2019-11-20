#!/usr/bin/python3

# The hadoop streaming process will most likely output the result into multiple files (1 for each reducer)
# in an output directory (usually Google Storage)
# This script will take all of these files in a specified directory and process them into separate one-column CSV
# files for each location, allowing us to create separate plots
# To make the data in to one column, we will strip the date
# We will also fill in missing data points for each location with an erroneous value (-1)
# The script is designed to work with any number of locations depending on the input, so minimal/no maintenance will be
# required for this script to use it for other locations

import sys
import tempfile
from os import makedirs
import glob
from google_storage_helpers import *
from weather import WeatherObservationLocation
import datetime


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

        # Create some temp directories to store the intermediate and output data locally for downloading/uploading
        temp_dir = tempfile.TemporaryDirectory()
        directory_path = path.abspath(path.join(temp_dir.name, "intermediate"))
        makedirs(directory_path, exist_ok=True)
        processed_output_dir = path.abspath(path.join(temp_dir.name, "output"))
        makedirs(processed_output_dir, exist_ok=True)

        download_from_gs(arg_directory_path, directory_path)
    else:
        print("Using local output directory")
        # Instead of using a temp directory, we can simply use the local directory, and we make sure the processed
        # output directory exists
        directory_path = path.abspath(arg_directory_path)
        processed_output_dir = path.abspath(arg_processed_output_dir)
        makedirs(processed_output_dir, exist_ok=True)

    processed_output_files = process_files(directory_path, processed_output_dir)

    print("%s Processed Files have been written to %s" % (len(processed_output_files), processed_output_dir))

    # If using Google Storage, we need to upload the results
    if arg_directory_path.startswith("gs://"):
        print("Uploading results to Google Storage")

        for location in processed_output_files:
            print("Uploading %s result file" % location)
            upload_to_gs(path.join(arg_processed_output_dir, location.name + ".csv"),
                         path.join(processed_output_dir, location.name + ".csv"))

        print("Cleaning up temporary directories")
        temp_dir.cleanup()


def process_files(directory_path, processed_output_dir):
    # Get all the files in the directory supplied,
    # Use list comprehension to ensure we dont pick up any directories that might be in this directory, and avoid the
    # _SUCCESS file that hadoop creates
    files = [file_path for file_path in glob.glob(directory_path + "/*")
             if path.isfile(file_path) and "_SUCCESS" not in file_path]
    print("Processing files")

    # Process the output data into a dictionary of values,
    # such that each location has its own list of sorted data points
    # Using dictionary and list comprehensions, we can initialise a dictionary of lists with all values of -1
    locations = [location for location in WeatherObservationLocation if location != WeatherObservationLocation.UNKNOWN]
    processed_output_files = {l: ["-1" for i in range(365)] for l in locations}
    for file_path in files:
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                key, value = line.split("\t")
                date, location = key.split(".")
                date = datetime.datetime.strptime(date, "%Y%m%d")

                # Convert the location string into a human-readable name for the file output
                try:
                    location = WeatherObservationLocation(location)
                except ValueError:
                    print("Could not find location '%s' in '%s' Enum" % (location, WeatherObservationLocation.name))

                # In order to deal with missing data points, we use the fact that the list is initialised with a
                # value for every day, then only insert and temperature difference value if we have a value for that
                # day in the year. This means the index of each element is equivalent to the day in the year.
                # This also has the affect of sorting the data into date order
                days_since_beginning = (date - datetime.datetime(2018, 1, 1)).days
                processed_output_files[location][days_since_beginning] = "%s" % value

    for location in processed_output_files:
        with open(path.join(processed_output_dir, location.name + ".csv"), "w+") as file:
            for line in processed_output_files[location]:
                file.write(line + "\n")
    return processed_output_files


if __name__ == "__main__":
    main(sys.argv)
