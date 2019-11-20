#!/usr/bin/env python3

# This class is essentially just a helper class to make the code in our mapper/reducer more readable,
# and improve the maintainability of the code by making it such that you only have to edit this single
# script to add new locations/measurements, you don't have to make any changes to the mapper/reducer itself

from enum import Enum


class WeatherObservationType(Enum):
    # TMIN and TMAX are the values used in the dataset to define the min/max temp observations
    TEMPERATURE_MAX = "TMAX"
    TEMPERATURE_MIN = "TMIN"
    # We don't currently care for any other element (reading) types, so we just mark them as unknown
    UNKNOWN = 0


class WeatherObservationLocation(Enum):
    OXFORD = "UK000056225"
    WADDINGTON = "UK000003377"
    # We don't currently care for any other locations, so just mark as unknown
    # To support other locations, all you need to do is add it as an entry into this enum, the rest of the program
    # will then support the new location and output a seperate csv file for it
    UNKNOWN = 0


class Observation:
    Location = None
    Date = None
    Type = None
    Temperature = None

    # Takes a line of data from the dataset and converts it into a object
    # These are the values we actually care about for each line, which will be supplied in this order
    #     station identifier (GHCN Daily Identification Number)
    #     date (yyyymmdd; where yyyy=year; mm=month; and, dd=day)
    #     observation type (see ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt for definitions)
    #     observation value (see ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt for units)
    def __init__(self, line):
        # Strip whitespace from the line
        line = line.strip()

        # Tokenize the line
        values = line.split(",")

        # Determine the location
        try:
            self.Location = WeatherObservationLocation(values[0])
        except ValueError as _:
            self.Location = WeatherObservationLocation.UNKNOWN
            return

        # Set the date
        self.Date = values[1]

        # Determine the type of observation
        try:
            self.Type = WeatherObservationType(values[2])
        except ValueError as _:
            self.Type = WeatherObservationType.UNKNOWN
            # Don't bother determining any more values, as this observation won't be used if the type is UNKNOWN
            return

        # Set the Temperature
        self.Temperature = values[3]
