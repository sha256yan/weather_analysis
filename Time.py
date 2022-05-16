import re
import pandas as pd
from datetime import datetime, date, time



class Time(pd.Series):
    """
        Parent of time types
    """
    def __init__(self, series):
        sorted_series = series.sort_values()
        super().__init__(sorted_series)
        self.time_objects = sorted_series.apply(self.process_string)

        
        
class Hours(Time):
    """
        23:59:59
    """
    @staticmethod
    def process_string(timestr):
        if type(timestr) != str:
            return None
        split_timestr = timestr.split(":")
        hour = int(split_timestr[0])
        minute = int(split_timestr[1])
        return time(hour, minute)
    
    def seconds_from_midnight(self):
        print(self.time_objects)
        seconds = self.time_objects.dropna().apply(lambda time_obj: time_obj.hour * 3600 + time_obj.minute * 60)
        return seconds
    
    
class Years(Time):
    """
        2022/01/01
    """
    @staticmethod
    def process_string(timestr):
        date_units = [int(date_unit) for date_unit in timestr.split("-")]
        return date(*date_units)
    
    
    def days_from_first(self):
        first_day = self.time_objects[0]
        days_from_first = self.time_objects.apply(lambda time_obj: (time_obj - first_day).days)
        return days_from_first




class DateTime(Time):
    """
        2022/01/01 23:59:59
    """
    @staticmethod
    def process_string(timestr):
        settlementdate_format = r'(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2})'
        re_time = re.match(settlementdate_format, timestr)
        time_object = datetime(*[int(time_unit) for time_unit in re_time.groups()])
        return time_object
        
        