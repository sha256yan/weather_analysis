from Time import Hours, Date, DateTime
from Series import Speed, Direction

import math
import pandas as pd
from datetime import timedelta


WEATHER_DIR = "./weather/"



class DataFrame(pd.DataFrame):
    """
        Parent for weather and price dataframe wrappers
    """
    def __init__(self, *args):
        processed_df = self.process_df(*args)
        super().__init__(processed_df)

        

        

        
        
class PriceDemand(DataFrame):
    """
        Container for price demand data.
    """
    
    @staticmethod
    def process_df(*args):
        price_demand = pd.read_csv(WEATHER_DIR + 'price_demand_data.csv')
        datetime_settlements = DateTime(price_demand["SETTLEMENTDATE"])
        price_demand["SETTLEMENTDATE"] = datetime_settlements#.time_objects
        year_dates = datetime_settlements.convert_to_year()
        price_demand["Date"] = year_dates
        return price_demand
   
    def get_grouped(price_demand):
        agg_params = {"TOTALDEMAND": "mean", "PRICESURGE": lambda surge_series: surge_series.loc[surge_series].size}
        grouped_price_demand = price_demand.groupby(["REGION", "Date"]).agg(agg_params)
        return grouped_price_demand

    
    
    
    
    

class City(DataFrame):
    """
        Container for a single city weather data
    """
    def process_df(*args):
        direction_columns = [
            "Direction of maximum wind gust ",
            "9am wind direction",
            "3pm wind direction"
        ]

        speed_columns = [
            "Speed of maximum wind gust (km/h)",
            "9am wind speed (km/h)",
            "3pm wind speed (km/h)"
        ]
        
        #args[0] is the instance, so need 1 and 2 for the df and state code arguements
        city_df = args[1]
        state_code = args[2]
        
        #adds a REGION column with the state code and replaces the Date col with desired datetime obj column
        city_df["REGION"] = state_code
        #city_df["Date"] = Date(city_df["Date"]).time_objects
        city_df["Time of maximum wind gust"] = Hours(city_df["Time of maximum wind gust"]).seconds_from_midnight()
        
        #changes speed and direction columns to form specified in wrapper classes
        for col in speed_columns:
            city_df[col] = Speed(city_df[col])
        for col in direction_columns:
            city_df[col] = Direction(city_df[col])
            
        city_df.set_index(["Date", "REGION"], inplace=True)
        return city_df
    

    
    
    

    
class Cities():
    
    @staticmethod
    def get_all_cities():
        """
            Loads all city weather dataframes and returns an array containing (city_df, state_code) tuples.
            i.e [ (city1, statecode1), (city2, statecode2) ... ]
        """
        CITY_SUFFIXES = ["_melbourne", "_sydney", "_adelaide", "_brisbane"]
        STATE_CODES = ["VIC1", "NSW1", "SA1", "QLD1"]
        CITY_DIRS = [WEATHER_DIR + "weather" + suffix + ".csv" for suffix in CITY_SUFFIXES]
        cities = []
        for i in range(len(CITY_DIRS)):
            #[(df, statecode), (df, statecode)]
            cities.append((pd.read_csv(CITY_DIRS[i]), STATE_CODES[i]))    
        return cities
    
    
    def __init__(self):
        cities_dfs = self.get_all_cities()
        self.df = CitiesDataFrame(cities_dfs)
        self.fake_values = pd.Series(dtype='object')
        self.date = Date(self.df["Date"])
        self.columns = self.df.columns
    
    def mean_fill_nans(self, columns):
        current_fakes = self.df.fill_nans(columns, self.date)
        self.fake_values = pd.concat([self.fake_values, *current_fakes])
        
    def fake_indexes(self, column):
        fake_value_indexes = self.fake_values.loc[self.fake_values == column].index
        return fake_value_indexes
    
    def get_fake_values(self, column):
        fake_value_indexes = self.fake_indexes(column)
        return self.df.loc[fake_value_indexes][column]
    
    def get_real_values(self, column):
        fake_value_indexes = self.fake_indexes(column)
        return self.df.drop(fake_value_indexes)[column]
    
    def get_days_from_first(self):
        return self.date.days_from_first()
    
    def get_first_day(self):
        return self.date[0]

    def join_price(self, grouped_price_demand):
        #returns a new df which is the join of cities and price demand
        return self.df.join(grouped_price_demand, on=["REGION", "Date"], how='right')
    

        

        
        
        
 
        
class CitiesDataFrame(DataFrame):
    """
        Container all of the cities' weather data.
    """
    
    
    
    def process_df(self, *args):
        cities_dataframes = args[0]
        City_array = [City(*city) for city in cities_dataframes]
        Cities_dataframe = pd.concat(City_array, axis=0).reset_index()
        return Cities_dataframe
    
    
    

    
    def nan_processor(self, nan_region, nan_date, column, date):
    
        date_objects = date.time_objects
        is_in_region = self["REGION"] == nan_region
        nan_date_object = Date.process_string(nan_date)

        lower_bound = nan_date_object - timedelta(days=10)
        upper_bound = nan_date_object + timedelta(days=10)

        date_is_close = (date_objects > lower_bound) & (date_objects < upper_bound)
        fill_value = self.loc[date_is_close & is_in_region][column].mean()

        if(math.isnan(fill_value)):
            fill_value = self.loc[date_is_close][column].mean()
        return fill_value

    
    
    
    def fill_nans(self, cols, date):
        current_fakes = []
        for col in cols:
            nans = self.loc[self[col].isna()][["REGION", "Date"]]
            nans_filled = nans.transpose().apply(lambda region_and_date: self.nan_processor(*region_and_date, col, date))


            if nans_filled.index.size > 2:
                current_fakes.append(pd.Series(data=col, index=nans_filled.index))
                self.loc[nans_filled.index, col] = nans_filled
        return current_fakes
    
    
    
    
