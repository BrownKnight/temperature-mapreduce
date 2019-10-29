# Run this script using "python3 plotter.py <path_to_data_csv_file>"
import csv
import sys
import matplotlib.pyplot as pyp

# Check the arguments are correct
# Number of arguments should be 2 (python script name is counted)
args = sys.argv
if len(args) != 2:
    print("Wrong number of arguments provided, desired syntax is:")
    print("python3 plotter.py <path_to_data_csv_file>")
    quit()

csv_path = args[1]

keys = []
values = []

with open(csv_path) as csv_file:
    csv_dict = csv.reader(csv_file, delimiter='\t')
    for row in csv_dict:
        keys.append(row[0].split('.')[0])
        values.append(int(row[1].split('.')[1]))

fig, axes = pyp.subplots()
axes.plot(keys, values)
pyp.show()
