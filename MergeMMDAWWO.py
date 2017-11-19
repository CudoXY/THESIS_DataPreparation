from enum import Enum

from DataToMerge import DataToMerge
import pandas as pd
import os


class MergeMMDAWWO(DataToMerge):
    class Columns:
        class Traffic(Enum):
            DATE_TIME = 'dt'
            LINE_NAME = 'lineName'
            STATION_NAME = 'stationName'

        class Weather(Enum):
            DATE_TIME = 'datetime'

    class SaveMode(Enum):
        BY_STATION = 1
        BY_LINE = 2

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

    def format(self):
        self.df.drop(self.Columns.Weather.DATE_TIME.value, axis=1, inplace=True)

    def save(self, save_path):
        temp_df = self.df.set_index(self.Columns.Traffic.DATE_TIME.value)
        temp_df.to_csv(save_path)

    def save_formatted(self, file_path_format, save_mode):
        col = self.Columns.Traffic.LINE_NAME.value if save_mode == self.SaveMode.BY_LINE else self.Columns.Traffic.STATION_NAME.value
        label_list = self.df[col].unique()

        for label in label_list:
            save_path = file_path_format.format(label=label)
            temp_df = self.df.loc[(self.df[col] == label)]
            temp_df.to_csv(save_path)
