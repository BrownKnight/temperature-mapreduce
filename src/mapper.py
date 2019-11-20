#!/usr/bin/python3

import sys
# This is required as a sort of "hack" to overcome the weird system path issues in hadoop streaming/gcloud dataproc
sys.path.append("./")
from weather import *

for line in sys.stdin:
    # We use a helper class to read each line of the dataset to make our code more readable, and easier to maintain
    # (i,e, add new locations in a single place for example)
    # However this does add a little overhead to the program - a compromise that I think is worth it
    observation = Observation(line)

    # Check to see if we care about this observation, otherwise continue to the next one
    if (observation.Location == WeatherObservationLocation.UNKNOWN
            or observation.Type == WeatherObservationType.UNKNOWN):
        # Not an observation we care about, so ignore and move on
        continue

    # Output the observation in the following format so Hadoop and the reducers can read the data
    # tabs are used to separate key/values in Hadoop MapReduce
    # "<Date>.<Location>\t<Type>.<Temperature>"
    # e.g. "20180101.OXFORD\tTEMPERATURE_MIN.18"
    print(
        "%s.%s\t%s.%s" % (observation.Date, observation.Location.value, observation.Type.name, observation.Temperature))
