#!/usr/bin/python3
# Run this script using "python3 plotter.py <path_to_data_csv_file>"
import datetime
import sys
from glob import glob
from os import path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from google_storage_helpers import download_from_gs
import tempfile


def main(args):
    # Check the number of arguments are correct
    # Number of arguments should be at least 2 (python script name is included in args)
    if len(args) < 2:
        print("At least one argument should be provided, desired syntax is:")
        print("python3 plotter.py <path_to_data_csv_file> <path_to_second_data_file> ...")
        quit()

    # Get all the arguments apart from the first one (as the first one is name of the script)
    arg_paths = args[1:]
    fig, ax = plt.subplots()

    # If we are given a Google Storage directory, we need to download the directory and use the paths to
    # those files instead
    if arg_paths[0].startswith("gs://"):
        if len(arg_paths) > 1:
            print("When downloading from Google Storage, only 1 GS directory is supported at a time")
            quit()

        # Create a temporary directory on the local computer for the GS files to be downloaded to
        temp_dir = tempfile.TemporaryDirectory()
        directory_path = path.abspath(path.join(temp_dir.name, "plotter_input"))
        download_from_gs(arg_paths[0], directory_path)

        # Redefine arg_paths as all the csv files in the new temp directory
        csv_file_paths = [file_path for file_path in glob(directory_path + "/*") if
                          path.isfile(file_path) and file_path.endswith(".csv")]
    else:
        csv_file_paths = arg_paths

    for csv_path in csv_file_paths:
        plot_from_csv_file(csv_path, ax, "r-")

    fig.autofmt_xdate()
    plt.show()

    # TODO upload back to GS if the file came from GS
    if arg_paths[0].startswith("gs://"):
        temp_dir.cleanup()


def plot_from_csv_file(csv_path, ax, line_format):
    str2date = lambda x: datetime.datetime.strptime(x.decode('ascii'), "%Y%m%d")
    r = np.recfromcsv(csv_path, delimiter="-", converters={0: str2date})

    keys = []
    values = []
    for record in r:
        keys.append(record[0])
        values.append(record[1])

    ax.plot(keys, values, line_format)

    months = mdates.MonthLocator()
    months_formatter = mdates.DateFormatter('%b-%Y')
    days = mdates.DayLocator()
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(months_formatter)
    ax.xaxis.set_minor_locator(days)
    ax.set_xlim(keys[0] - datetime.timedelta(1), keys[-1])
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = lambda x: '%1.1f' % x


if __name__ == "__main__":
    main(sys.argv)
