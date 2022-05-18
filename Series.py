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
    
    def __init__(self, speed_series):
        not_calm = speed_series.loc[speed_series != "Calm"]
        if(speed_series.dtype == "float64"):
            processed = not_calm.dropna()
        processed = pd.to_numeric(not_calm.dropna())
        super().__init__(processed)
        
    
    

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
    
    def __init__(self, direction_series):
        processed = direction_series.apply(lambda direction: self.direction_lookup.get(direction, None)).dropna()
        super().__init__(processed)
    

