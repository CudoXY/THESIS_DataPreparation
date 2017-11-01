from enum import Enum

from DataToPrepare import DataToPrepare
import pandas as pd


class MMDATrafficData(DataToPrepare):
    class Columns():
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

    def normalize(self):
        pass

    def interpolate(self):
        return

    def format(self):
        # Remove lineID, stationID, timestamp columns
        self.df.drop(self.df.columns[:2], axis=1, inplace=True)
        self.df.drop(self.Columns.Traffic.TIMESTAMP.value, axis=1, inplace=True)

        print(self.df.head())

    def __init__(self, line_name_path, line_station_path, traffic_data_path, line_name_filter_list = [], station_name_filter_list = []):
        self.df = pd.DataFrame()
        self.load(traffic_data_path)
        self.merge_line_names(line_name_path)
        self.merge_line_stations(line_station_path)
        self.format()
        self.filter()
        self.interpolate()
        # self.normalize()

    def save(self, save_path):
        self.df.to_csv(save_path)

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
                           right_on=[self.Columns.LineStations.LINE_ID.value, self.Columns.LineStations.STATION_ID.value],
                           how='left')

        # print(self.df.head(100).to_string())

    def filter(self):
        pass
