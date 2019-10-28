from enum import Enum


class WeatherObservationType(Enum):
    # TMIN and TMAX are the values used in the dataset to define the min/max temp observations
    TemperatureMax = "TMAX"
    TemperatureMin = "TMIN"
    #   We don't care for any other element (reading) types, so we just mark them as unknown
    UNKNOWN = 0


class WeatherObservationLocation(Enum):
    Oxford = "UK000056225"
    Waddington = "UK000003377"
    #   We don't care for any other locations, so just mark as unknown
    UNKNOWN = 0


class WeatherObservation:

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
        if values[0] == WeatherObservationLocation.Oxford.value:
            self.Location = WeatherObservationLocation.Oxford
        elif values[0] == WeatherObservationLocation.Waddinton.value:
            self.Location = WeatherObservationLocation.Waddinton
        else:
            self.Location = WeatherObservationLocation.UNKNOWN
            # If it's not a location we care about, don't bother determining any other values, as this observation
            # will be ignored
            return

        # Set the date
        self.Date = values[1]

        # Determine the type of observation
        if values[2] == WeatherObservationType.TemperatureMax.value:
            self.Type = WeatherObservationType.TemperatureMax
        elif values[2] == WeatherObservationType.TemperatureMin.value:
            self.Type = WeatherObservationType.TemperatureMin
        else:
            self.Type = WeatherObservationType.UNKNOWN
            # Don't bother determining any more values, as this observation won't be used if the type is UNKNOWN
            return

        # Set the Temperature
        self.Temperature = values[3]