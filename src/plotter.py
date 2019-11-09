#!/usr/bin/python3
# Run this script using "python3 plotter.py <path_to_data_csv_file>"
import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def main(args):
    # Check the number of arguments are correct
    # Number of arguments should be at least 2 (python script name is included in args)
    if len(args) < 2:
        print("At least one argument should be provided, desired syntax is:")
        print("python3 plotter.py <path_to_data_csv_file> <path_to_second_data_file> ...")
        quit()

    # Get all the arguments apart from the first one (as the first one is name of the script)
    csv_paths = args[1:]
    fig, ax = plt.subplots()

    plot_from_csv_file(csv_paths[1], ax, "r-")

    fig.autofmt_xdate()
    plt.show()


def plot_from_csv_file(csv_path, ax, line_format):
    str2date = lambda x: datetime.datetime.strptime(x.decode('ascii'), "%Y%m%d")
    r = np.recfromcsv(csv_path, delimiter="-", converters={0: str2date})

    keys = []
    values = []
    for record in r:
        keys.append(record[0])
        values.append(record[1])

    ax.plot("Date", "Temperature Difference", keys, values, line_format)

    months = mdates.MonthLocator()
    months_formatter = mdates.DateFormatter('%b-%Y')
    days = mdates.DayLocator()
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(months_formatter)
    ax.xaxis.set_minor_locator(days)
    ax.set_xlim(datetime.datetime(2018, 1, 1), datetime.datetime(2019, 1, 1))
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = lambda x: '%1.1f' % x


if __name__ == "__main__":
    main(sys.args)
