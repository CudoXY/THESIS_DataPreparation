from enum import Enum

from DataToPrepare import DataToPrepare
import pandas as pd
import numpy as np


class MMDATrafficData(DataToPrepare):
    class Columns:
        class Traffic(Enum):
            LINE_ID = 'lineID'
            STATION_ID = 'stationID'
            STATUS_NORTHBOUND = 'statusN'
            STATUS_SOUTHBOUND = 'statusS'
            TIMESTAMP = 'timestamp'
            DATE_TIME = 'dt'

        class LineNames(Enum):
            LINE_ID = 'lineID'
            STATION_COUNT = 'nStation'
            URL_KEY = 'URLKey'
            LINE_NAME = 'lineName'

        class LineStations(Enum):
            LINE_ID = 'lineID'
            STATION_ID = 'stationID'
            STATION_NAME = 'stationName'

    TRAFFIC_COND_RANKED_LIST = ['L', 'M', 'H']
    TRAFFIC_COND_NONE = 'N'

    def __init__(self, line_name_path, line_station_path, traffic_data_path, line_name_filter_list=[],
                 station_name_filter_list=[]):
        self.df = pd.DataFrame()
        self.load(traffic_data_path)
        self.merge_line_names(line_name_path)
        self.merge_line_stations(line_station_path)
        self.format()
        self.filter(line_name_filter_list, station_name_filter_list)
        self.interpolate()
        self.normalize()

    def normalize(self):
        pass

    def interpolate(self):
        # Remove northbound N labels
        self.df[self.Columns.Traffic.STATUS_NORTHBOUND.value] = np.where(
            self.df[self.Columns.Traffic.STATUS_NORTHBOUND.value] == self.TRAFFIC_COND_NONE,
            np.nan, self.df[self.Columns.Traffic.STATUS_NORTHBOUND.value])

        # Remove southbound N labels
        self.df[self.Columns.Traffic.STATUS_SOUTHBOUND.value] = np.where(
            self.df[self.Columns.Traffic.STATUS_SOUTHBOUND.value] == self.TRAFFIC_COND_NONE,
            np.nan, self.df[self.Columns.Traffic.STATUS_SOUTHBOUND.value])

        # Convert northbound labels to ranked value
        for i, weather_cond in enumerate(self.TRAFFIC_COND_RANKED_LIST):
            self.df[self.Columns.Traffic.STATUS_NORTHBOUND.value] = np.where(
                self.df[self.Columns.Traffic.STATUS_NORTHBOUND.value] == weather_cond,
                str(i / (len(self.TRAFFIC_COND_RANKED_LIST) - 1)),
                self.df[self.Columns.Traffic.STATUS_NORTHBOUND.value])

        # Convert southbound labels to ranked value
        for i, weather_cond in enumerate(self.TRAFFIC_COND_RANKED_LIST):
            self.df[self.Columns.Traffic.STATUS_SOUTHBOUND.value] = np.where(
                self.df[self.Columns.Traffic.STATUS_SOUTHBOUND.value] == weather_cond,
                str(i / (len(self.TRAFFIC_COND_RANKED_LIST) - 1)),
                self.df[self.Columns.Traffic.STATUS_SOUTHBOUND.value])

        self.df[self.Columns.Traffic.STATUS_NORTHBOUND.value] = self.df[
            self.Columns.Traffic.STATUS_NORTHBOUND.value].astype(float)
        self.df[self.Columns.Traffic.STATUS_SOUTHBOUND.value] = self.df[
            self.Columns.Traffic.STATUS_SOUTHBOUND.value].astype(float)
        self.df = self.df.interpolate(method='linear')

    def format(self):
        # Remove lineID, stationID, timestamp columns
        self.df.drop(self.df.columns[:2], axis=1, inplace=True)
        self.df.drop(self.Columns.Traffic.TIMESTAMP.value, axis=1, inplace=True)

    def save(self, save_path):
        temp_df = self.df.set_index(self.Columns.Traffic.DATE_TIME.value)
        temp_df.to_csv(save_path)

    def load(self, traffic_data_path):
        # Load CSV File
        self.df = pd.read_csv(traffic_data_path, sep=',\s,', delimiter=',', skipinitialspace=True)

        # print(self.df.head())

    def merge_line_names(self, line_name_path):
        # Load CSV File
        line_name_df = pd.read_csv(line_name_path, sep=',\s,', delimiter=',', skipinitialspace=True)

        # Remove '#' symbol on column headers
        line_name_df.columns = line_name_df.columns.str.replace('#', '')

        # Merge with Traffic Data
        self.df = pd.merge(self.df, line_name_df[[self.Columns.LineNames.LINE_ID.value,
                                                  self.Columns.LineNames.LINE_NAME.value]],
                           left_on=[self.Columns.Traffic.LINE_ID.value],
                           right_on=[self.Columns.LineNames.LINE_ID.value],
                           how='inner')

        # print(self.df.head().to_string())

    def merge_line_stations(self, line_station_path):
        # Load CSV File
        line_station_df = pd.read_csv(line_station_path, sep=',\s,', delimiter=',', skipinitialspace=True)

        # Remove '#' symbol on column headers
        line_station_df.columns = line_station_df.columns.str.replace('#', '')

        # Merge with Traffic Data
        self.df = pd.merge(self.df, line_station_df,
                           left_on=[self.Columns.Traffic.LINE_ID.value, self.Columns.Traffic.STATION_ID.value],
                           right_on=[self.Columns.LineStations.LINE_ID.value,
                                     self.Columns.LineStations.STATION_ID.value],
                           how='left')
        # print(self.df.head(100).to_string())

    def filter(self, line_name_filter_list, station_name_filter_list):
        self.df = self.df.loc[(self.df[self.Columns.LineNames.LINE_NAME.value].isin(line_name_filter_list) |
                               self.df[self.Columns.LineStations.STATION_NAME.value].isin(station_name_filter_list))]
