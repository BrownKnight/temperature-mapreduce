#!/usr/bin/python3

import sys

# This is required as a sort of "hack" to overcome the weird system path issues in hadoop streaming/gcloud dataproc
sys.path.append("./")
from weather import *

# We will use -9999 as an error value, so it is obvious in the output if there is some erroneous value
last_temp = -9999
last_key = None
last_observation_type = WeatherObservationType.UNKNOWN

# Read in each line that has been sent to this particular reducer
for line in sys.stdin:
    line = line.strip()
    # Input will look something like 20180101.OXFORD \t TMIN.230, so here we process that into useful separate values
    current_key, value = line.split("\t", 1)
    current_observation_type, current_temp = value.split(".")

    current_temp = int(current_temp)

    # If the current key is the same as the previous, this means we have got two temperature readings for the same day
    # and thus can process the difference
    # Keys are always the same for date & location combinations
    if current_key == last_key:
        temp_difference = abs(current_temp - last_temp)

        # If the observation doesn't have a min & max but instead an min/max & avg, we can assume the actual
        # temperature difference for the day is 2*(difference between min/max & avg)
        # This requires us to make the assumption that the average temperature for the day is calculated by the
        # formula (max-min)/2
        if current_observation_type == WeatherObservationType.TEMPERATURE_AVG \
                or last_observation_type == WeatherObservationType.TEMPERATURE_AVG:
            temp_difference = temp_difference * 2

        # The temperature so far has been processed in tenths of degrees, b ut we want to output in
        # whole degrees with a decimal point
        temp_difference = temp_difference / 10

        # We place a dash between the key/value instead of a comma do create a 1 column csv instead of a 2 column file,
        # to satisfy the requirement in the specification
        # This will need to be processed by the plotter to interpret the single column in the csv as 2 distinct values
        print("%s-%s" % (current_key, temp_difference))

        # Reset the last_temp to the error value
        last_temp = -9999
        last_observation_type = WeatherObservationType.UNKNOWN
    else:
        last_temp = current_temp
        last_key = current_key
        last_observation_type = current_observation_type
