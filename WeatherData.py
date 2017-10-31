from abc import ABC, abstractmethod
import pandas as pd


class WeatherData(ABC):
    def __init__(self, file_path_format, year):
        self.df = pd.DataFrame()
        self.merge_weather_data(file_path_format, year)
        self.format()
        self.interpolate()
        self.normalize()

    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def interpolate(self):
        pass

    def save(self, save_path):
        self.df.to_csv(save_path)

    def merge_csv(self, csv_path):
        # Load CSV File
        csv_df = pd.read_csv(csv_path, sep=',\s,', delimiter=',', skipinitialspace=True)

        return pd.concat([self.df, csv_df], axis=0)

    def merge_weather_data(self, file_path_format, year):
        self.df = pd.DataFrame()
        for i in range(1, 13):
            csv_path = file_path_format.format(month=i, year=year)

            self.df = self.merge_csv(csv_path)
            print(len(self.df))
        return self.df
