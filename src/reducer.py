#!/usr/bin/python3

import sys

# This is required as a sort of "hack" to overcome the weird system path issues in hadoop streaming/gcloud dataproc
sys.path.append("./")
from weather import WeatherObservationType

# We will use -99999 as an error value, so it is obvious in the output if there is some erroneous value
last_temp = -99999
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

        # The temperature so far has been processed in tenths of degrees, but we want to output in
        # whole degrees with a decimal point
        temp_difference = temp_difference / 10.0

        # If the temp difference is more than 900, then this will be an erroneous value 
        if temp_difference < 9000:
            # Output format: "<Date>.<Location>\t<Temperature_Difference>" e.g. "20180101.UK0000562251    10"
            print("%s\t%s" % (current_key, temp_difference))

        # Reset the last_temp to the error value
        last_temp = -99999
        last_observation_type = WeatherObservationType.UNKNOWN
    else:
        last_temp = current_temp
        last_key = current_key
        last_observation_type = current_observation_type
