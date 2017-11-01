from abc import ABC, abstractmethod

import pandas as pd


class DataToMerge(ABC):
    def __init__(self, traffic_data_path, weather_data_path):
        self.df = pd.DataFrame()
        self.TRAFFIC_DATA_PATH = traffic_data_path
        self.WEATHER_DATA_PATH = weather_data_path
        self.load()
        self.merge()
        self.format()
        self.save()

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def merge(self):
        pass

    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def save(self):
        pass
