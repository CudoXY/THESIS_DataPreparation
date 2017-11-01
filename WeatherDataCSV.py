from abc import abstractmethod

import pandas as pd

from WeatherData import WeatherData


class WeatherDataCSV(WeatherData):

    def save(self, save_path):
        self.df.to_csv(save_path)

    def merge_csv(self, csv_path):
        # Load CSV File
        csv_df = pd.read_csv(csv_path, sep=',\s,', delimiter=',', skipinitialspace=True)

        return pd.concat([self.df, csv_df], axis=0)

    def merge(self):
        self.df = pd.DataFrame()
        for i in range(1, 13):
            csv_path = self.FILE_PATH_FORMAT.format(month=i, year=self.YEAR)

            self.df = self.merge_csv(csv_path)
            print(len(self.df))
        return self.df
