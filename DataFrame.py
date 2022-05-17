from Time import Hours, Date, DateTime
import pandas as pd

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
        year_dates = DateTime(price_demand["SETTLEMENTDATE"]).convert_to_year()
        price_demand["Date"] = year_dates
        return price_demand
   
    def get_grouped(price_demand):
        agg_params = {"TOTALDEMAND": "sum", "PRICESURGE": lambda surge_series: surge_series.loc[surge_series].size}
        grouped_price_demand = price_demand.groupby(["REGION", "Date"]).agg(agg_params)
        return grouped_price_demand

    
    
    
    
class City(DataFrame):
    """
        Container for a single city weather data
    """
    def process_df(*args):
        city_df = args[1]
        state_code = args[2]
        city_df["REGION"] = state_code
        city_df["Date"] = Date(city_df["Date"]).time_objects
        city_df.set_index(["Date", "REGION"], inplace=True)
        return city_df

    
    
    
class Cities(DataFrame):
    """
        Container all of the cities' weather data.
    """
    
    @staticmethod
    def get_all_cities():
        CITY_SUFFIXES = ["_melbourne", "_sydney", "_adelaide", "_brisbane"]
        STATE_CODES = ["VIC1", "NSW1", "SA1", "QLD1"]
        CITY_DIRS = [WEATHER_DIR + "weather" + suffix + ".csv" for suffix in CITY_SUFFIXES]
        cities = []
        for i in range(len(CITY_DIRS)):
            #[(df, statecode), (df, statecode)]
            cities.append((pd.read_csv(CITY_DIRS[i]), STATE_CODES[i]))    
        return cities
    
    
    @staticmethod
    def process_df(*args):
        cities_dataframes = Cities.get_all_cities()
        City_array = [City(*city) for city in cities_dataframes]
        Cities_dataframe = pd.concat(City_array, axis=0).reset_index()
        """
            TO DO:
                IMPLEMENT CLEANING ON THE COLUMNS. USE SERIES WRAPPERS.
                
        """
        return Cities_dataframe


    def price_join(self, grouped_price_demand):
        return self.join(grouped_price_demand, on=["REGION", "Date"], how='right')