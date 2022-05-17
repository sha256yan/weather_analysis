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


    

