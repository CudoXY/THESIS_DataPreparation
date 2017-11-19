from enum import Enum

import numpy as np
import pandas as pd

from WeatherDataCSV import WeatherDataCSV


class WWOData(WeatherDataCSV):
    class Columns(Enum):
        DATE = 'date'  # dd/MM/yyyy format
        TIME = 'time'  # int format (0, 100, 2300)
        DATE_TIME = 'datetime'  # int format (0, 100, 2300)
        TEMP_C = 'tempC'
        TEMP_F = 'tempF'
        WINDSPEED_MILES = 'windspeedMiles'
        WINDSPEED_KMPH = 'windspeedKmph'
        WINDDIR_DEGREE = 'winddirDegree'
        # WINDDIR_16POINT = 'winddir16Point'
        WEATHER_COND = 'cond'
        PRECIP = 'precipMM'
        HUMIDITY = 'humidity'
        VISIBILITY = 'visibility'
        PRESSURE = 'pressure'
        CLOUDCOVER = 'cloudcover'
        HEATINDEX_C = 'heatIndexC'
        HEATINDEX_F = 'heatIndexF'
        DEWPOINT_C = 'dewPointC'
        DEWPOINT_F = 'dewPointF'
        WINDCHILL_C = 'windChillC'
        WINDCHILL_F = 'windChillF'
        WINDGUST_MILES = 'windGustMiles'
        WINDGUST_KMPH = 'windGustKmph'
        FEELSLIKE_C = 'feelsLikeC'
        FEELSLIKE_F = 'feelsLikeF'

    WEATHER_COND_RANKED_LIST = ['Clear',
                                'Cloudy',
                                'Heavy rain',
                                'Heavy rain at times',
                                'Light drizzle',
                                'Light rain',
                                'Light rain shower',
                                'Mist',
                                'Moderate or heavy rain shower',
                                'Moderate rain',
                                'Moderate rain at times',
                                'Overcast',
                                'Partly cloudy',
                                'Patchy light drizzle',
                                'Patchy light rain',
                                'Patchy light rain with thunder',
                                'Patchy rain possible',
                                'Sunny',
                                'Thundery outbreaks possible',
                                'Torrential rain shower']

    def read_csv(self, csv_path):

        cols_to_read = [2]
        cols_to_read.extend(range(14, 39))

        # Exclude weather code and URL value
        cols_to_read.remove(20)
        cols_to_read.remove(21)
        cols_to_read.remove(22)

        csv_df = pd.read_csv(csv_path, sep=',\s,', delimiter=',', skipinitialspace=True, usecols=cols_to_read)
        return csv_df

    def format(self):

        # Rename columns
        self.df.columns = [
            self.Columns.DATE.value,
            self.Columns.TIME.value,
            self.Columns.TEMP_C.value,
            self.Columns.TEMP_F.value,
            self.Columns.WINDSPEED_MILES.value,
            self.Columns.WINDSPEED_KMPH.value,
            self.Columns.WINDDIR_DEGREE.value,
            # self.Columns.WINDDIR_16POINT.value,
            self.Columns.WEATHER_COND.value,
            self.Columns.PRECIP.value,
            self.Columns.HUMIDITY.value,
            self.Columns.VISIBILITY.value,
            self.Columns.PRESSURE.value,
            self.Columns.CLOUDCOVER.value,
            self.Columns.HEATINDEX_C.value,
            self.Columns.HEATINDEX_F.value,
            self.Columns.DEWPOINT_C.value,
            self.Columns.DEWPOINT_F.value,
            self.Columns.WINDCHILL_C.value,
            self.Columns.WINDCHILL_F.value,
            self.Columns.WINDGUST_MILES.value,
            self.Columns.WINDGUST_KMPH.value,
            self.Columns.FEELSLIKE_C.value,
            self.Columns.FEELSLIKE_F.value]

        # Merge date and time
        self.df[self.Columns.DATE_TIME.value] = pd.to_datetime(self.df[self.Columns.DATE.value].apply(str) + ' ' +
                                                               self.df[self.Columns.TIME.value].apply(str).apply(lambda x: x.zfill(4)),
                                                               format='%d/%m/%Y %H%M')

        # Remove date and time column
        self.df.drop([self.Columns.DATE.value, self.Columns.TIME.value], axis=1, inplace=True)

        # Set datetime as index
        self.df.set_index([self.Columns.DATE_TIME.value], inplace=True)

    def interpolate(self):
        # print(self.df.head().to_string())

        print(self.df.index.get_level_values(self.Columns.DATE_TIME.value).get_duplicates())

        # Convert labels to ranked value
        for i, weather_cond in enumerate(self.WEATHER_COND_RANKED_LIST):
            self.df[self.Columns.WEATHER_COND.value] = np.where(
                self.df[self.Columns.WEATHER_COND.value] == weather_cond,
                str(i / (len(self.WEATHER_COND_RANKED_LIST) - 1)), self.df[self.Columns.WEATHER_COND.value])

        self.df[self.Columns.WEATHER_COND.value] = self.df[self.Columns.WEATHER_COND.value].astype(float)
        print(len(self.df))
        self.df = self.df.resample('15T')
        self.df = self.df.interpolate(method='linear')

        self.df = self.df[:-1]
        print(len(self.df))
        # print(self.df.head(96).to_string())

    def normalize(self):
        # Get all unique weather condition values
        # weather_cond_col_list = self.df.time_weather.unique()

        # for weather_cond_col in weather_cond_col_list:
        #     self.df[weather_cond_col] = np.where(
        #         self.df[self.Columns.WEATHER_CONDITION.value] == weather_cond_col, 1, 0)

        self.df = (self.df - self.df.min()) / (self.df.max() - self.df.min())

        print(self.df.head(10).to_string())
