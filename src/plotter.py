#!/usr/bin/python3
# Run this script using "python3 plotter.py <path_to_data_csv_file>"
import datetime
import sys
from glob import glob
from os import path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from google_storage_helpers import download_from_gs, upload_to_gs
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

    csv_file_paths, temp_dir = get_csv_file_paths(arg_paths)

    # Set the size of the figure to 1/3rd the height of an A4 page, and the full width of an A4 page
    fig, ax = plt.subplots(figsize=(8, 3.8), dpi=150, nrows=len(arg_paths) - 1, ncols=1)

    # Give the plots upto 4 different colours, to make it easier to differentiate them

    possible_plot_formats = ["b-", "g-", "r-", "y-"]

    for index, csv_path in enumerate(csv_file_paths):
        plot_from_csv_file(csv_path, fig.axes[index], possible_plot_formats[index % 4])

    fig.autofmt_xdate()
    plt.show()

    # Output the plot as a file, to the directory specified in the program arguments
    output_figure_to_file(arg_paths, fig, temp_dir)

    # Cleanup the temp directory that would've been made if downloading from Google Storage
    if arg_paths[0].startswith("gs://") or arg_paths[-1].startswith("gs://"):
        temp_dir.cleanup()


def get_csv_file_paths(arg_paths):
    # If we are using Google Storage to download or upload files to, we need a temporary directory for files
    # to be downloaded to/uploaded from
    temp_dir = None
    if arg_paths[0].startswith("gs://") or arg_paths[-1].startswith("gs://"):
        temp_dir = tempfile.TemporaryDirectory()

    # If we are given a Google Storage directory, we need to download the directory and use the paths to
    # those files instead
    if arg_paths[0].startswith("gs://"):
        # There should only be two arguments when using GS, a path to download and a path to upload
        if len(arg_paths) != 2:
            print("When downloading from Google Storage, only 1 GS directory to download from is supported at a time")
            print("Desired Syntax: python3 plotter.py <google_storage_path_to_download> <google_storage_path_to_upload")
            quit()

        directory_path = path.abspath(path.join(temp_dir.name, "plotter_input"))
        download_from_gs(arg_paths[0], directory_path)

        # Redefine arg_paths as all the csv files in the new temp directory
        csv_file_paths = [file_path for file_path in glob(directory_path + "/*") if
                          path.isfile(file_path) and file_path.endswith(".csv")]
    else:
        # Use all but the last path as the last one is the output path
        csv_file_paths = arg_paths[:-1]

    return csv_file_paths, temp_dir


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
    ax.xlabel = "Date"
    ax.ylabel = "Temperature Difference"
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = lambda x: '%1.1f' % x


def output_figure_to_file(arg_paths, fig, temp_dir):
    if arg_paths[-1].startswith("gs://"):
        plot_file_path = path.abspath(path.join(temp_dir.name, "plotter_output.png"))
    else:
        plot_file_path = path.abspath(path.join(arg_paths[-1], "plotter_output.png"))
    fig.savefig(plot_file_path)
    # If the last path given to the script is a Google Storage path, then upload the plot there
    if arg_paths[-1].startswith("gs://"):
        upload_to_gs(path.join(arg_paths[1], "plots.png"), plot_file_path)


if __name__ == "__main__":
    main(sys.argv)
