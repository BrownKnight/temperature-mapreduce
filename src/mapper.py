#!/usr/bin/python3

import sys
from weather import *

for line in sys.stdin:
    observation = Observation(line)

    # Check to see if we care about this observation, otherwise continue to the next one
    if (observation.Location == WeatherObservationLocation.UNKNOWN
            or observation.Type == WeatherObservationType.UNKNOWN):
        # Not an observation we care about, so ignore and move on
        continue

    # Output the observation in the following format so the reducers can read the data
    # "<Date>.<Location>\t<Type>.<Temperature>"
    # e.g. "20180101.Oxford\tTemperatureMin.18"
    print(
        "%s.%s\t%s.%s" % (observation.Date, observation.Location.name, observation.Type.name, observation.Temperature))
