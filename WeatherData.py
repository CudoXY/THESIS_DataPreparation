from DataToPrepare import DataToPrepare
from abc import abstractmethod
import pandas as pd


class WeatherData(DataToPrepare):

    @abstractmethod
    def merge(self):
        pass

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def interpolate(self):
        pass

    @abstractmethod
    def format(self):
        pass

    def __init__(self, file_path_format, year):
        self.FILE_PATH_FORMAT = file_path_format
        self.YEAR = year
        self.df = pd.DataFrame()
        self.merge()
        self.format()
        self.interpolate()
        self.normalize()

    def save(self, save_path):
        self.df.to_csv(save_path)
