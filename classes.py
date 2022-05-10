import pandas as pd
from datetime import date


"""
    wind speed (km/h) note: values are strings. Some entries are "Calm". Others "30.00" floatish
    wind direction (Compass direction) 
    MSL pressure (hPa) hecto Pascal = 100 Pascal
    
    
    Celsius
    mm
    hours
    direction
    percentage
    oktas
    hPa
    km/h
    date
    time
"""
 
class Speed(pd.Series):
    def process(self):
        if(self.dtype == "float64"):
            return self.loc[self != "Calm"].dropna()
        return pd.to_numeric(self.loc[self != "Calm"].dropna())
    
    

    
    
    
    

class Direction(pd.Series):
    direction_lookup = {
        "S": 270.0,
        "SSW": 247.5,
        "SE": 315.0,
        "NNW": 112.5,
        "NW": 135.0,
        "SW": 225.0,
        "N": 90.0,
        "SSE": 292.5,
        "WSW": 202.5,
        "ESE": 337.5,
        "E": 0.0,
        "NNE": 67.5,
        "WNW": 157.5,
        "W": 180.0,
        "NE": 45.0,
        "ENE": 22.5
    }
    #self.direction_lookup.get(direction, None)
    def process(self):
        return self.dropna().apply(lambda direction: self.direction_lookup.get(direction, None)).dropna()


    

    

class Time(pd.Series):
    
    @staticmethod
    def HM_to_seconds(time):
        """
            Returns seconds after midnight for an individual 
            time string of the form "hh:mm".
        """
        times = time.split(":")
        hour = int(times[0])
        minute = int(times[1])
        seconds_after_midnight = 60 * (hour * 60  + minute)
        return seconds_after_midnight
    
    @staticmethod
    def datetime_from_str(time_string):
        """
            Takes in a string in the form "2022-03-22"
            and returns a corresponding datetime date object
        """
        return date(*[int(time) for time in time_string.split("-")]) 
    
    def sec_after_midnight(self):
        """
            Converts a series with values of the form 'hh:mm' to 
            seconds after midnight aka '00:00' for each time value.
        """
        return self.dropna().apply(lambda timestr: self.HM_to_seconds(timestr))
    
    def days_after_min(self):
        """
            Takes a series containing strings in the form "2022-03-22"
            and returns an array of integers representing number of days since
            the earliest date in the series.
            i.e. if the earliest date in the series is 2022-03-22, the position
            in the time-difference array corresponding to 2022-03-26 will be 4 
            since 03-26 is 4 days after the earliest date, 03-22.
        """
        datetimes = self.apply(lambda time_string: self.datetime_from_str(time_string))
        time_differences = [(datetime-datetimes[0]).days for datetime in datetimes]
        return time_differences