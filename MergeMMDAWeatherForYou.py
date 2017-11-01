from enum import Enum

from DataToMerge import DataToMerge
import pandas as pd
import numpy as np


class MergeMMDAWeatherForYou(DataToMerge):
    class Columns:
        class Traffic(Enum):
            LINE_ID = 'lineID'
            STATION_ID = 'stationID'
            STATUS_NORTHBOUND = 'statusN'
            STATUS_SOUTHBOUND = 'statusS'
            DATE_TIME = 'dt'
            LINE_NAME = 'lineName'
            STATION_NAME = 'stationName'

        class Weather(Enum):
            DATE_TIME = 'date_time'
            WEATHER_CONDITION = 'time_weather'
            TEMPERATURE = 'time_temp'  # Farenheit
            DEW_POINT = 'time_dewpt'  # Farenheit
            HUMIDITY = 'time_hum'  # Percent
            PRESSURE = 'time_pressure'
            WIND_SPEED = 'time_winds'  # MPH

    def __init__(self, traffic_data_path, weather_data_path):
        self.traffic_df = pd.DataFrame()
        self.weather_df = pd.DataFrame()
        super().__init__(traffic_data_path, weather_data_path)

    def load(self):
        # Load CSV File
        self.traffic_df = pd.read_csv(self.TRAFFIC_DATA_PATH, sep=',\s,', delimiter=',', skipinitialspace=True)
        self.weather_df = pd.read_csv(self.WEATHER_DATA_PATH, sep=',\s,', delimiter=',', skipinitialspace=True)

    def merge(self):

        # Merge with Traffic Data
        self.df = pd.merge(self.traffic_df, self.weather_df,
                           left_on=self.Columns.Traffic.DATE_TIME.value,
                           right_on=self.Columns.Weather.DATE_TIME.value,
                           how='left')

        # Dispose traffic and weather dataframes
        del self.traffic_df
        del self.weather_df

        print(self.df.head().to_string())

    def save(self):
        pass

    def format(self):
        pass
