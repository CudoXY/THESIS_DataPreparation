from enum import Enum

import numpy as np
import pandas as pd

from WeatherDataCSV import WeatherDataCSV


class WeatherForYou(WeatherDataCSV):
    class Columns(Enum):
        DATE_TIME = 'date_time'
        MONTH = 'time_month'
        DAY = 'time_date'
        YEAR = 'time_year'
        TIME = 'time_name'  # Format: H:Mp
        WEATHER_CONDITION = 'time_weather'
        TEMPERATURE = 'time_temp'  # Farenheit
        DEW_POINT = 'time_dewpt'  # Farenheit
        HUMIDITY = 'time_hum'  # Percent
        PRESSURE = 'time_pressure'
        WIND_SPEED = 'time_winds'  # MPH

    WEATHER_COND_RANKED_LIST = ['Mostly Clear',
                                'Mostly Cloudy',
                                'Cloudy',
                                'Partly Cloudy',
                                'Haze',
                                'Hazy',
                                'Fog',
                                'Mist and Fog',
                                'Light Rain',
                                'Showers Nearby',
                                'Showers',
                                'Rain Showers',
                                'Scattered Showers',
                                'Rain',
                                'Heavy Rain',
                                'Scattered Storms',
                                'Light Thunderstorms',
                                'Thunderstorms',
                                'Heavy Thunderstorms']

    WEATHER_COND_SMOKE = 'Smoke'

    def format(self):
        # Format time_temp column
        self.df[self.Columns.TEMPERATURE.value] = self.df[self.Columns.TEMPERATURE.value].str.replace('°F', '') \
            .replace(r'\s+', '', regex=True) \
            .replace('', np.nan) \
            .fillna(method='pad').astype(int)

        # Format dew point column
        self.df[self.Columns.DEW_POINT.value] = self.df[self.Columns.DEW_POINT.value].str.replace('°F', '') \
            .replace(r'\s+', '', regex=True) \
            .replace('', np.nan) \
            .fillna(method='pad').astype(int)

        # Format humidity column
        self.df[self.Columns.HUMIDITY.value] = self.df[self.Columns.HUMIDITY.value].str.replace('%', '') \
            .replace(r'\s+', '', regex=True) \
            .replace('', np.nan) \
            .fillna(method='pad').astype(int)

        # Format wind speed column
        self.df[self.Columns.WIND_SPEED.value] = self.df[self.Columns.WIND_SPEED.value].str.replace(' MPH', '') \
            .replace(r'[\D\s]+', '', regex=True) \
            .replace('', np.nan) \
            .fillna(method='pad').astype(int)
        # print(self.df.head())

    def interpolate(self):
        # Combine month, day, year, time
        self.df[self.Columns.DATE_TIME.value] = pd.to_datetime(self.df[self.Columns.MONTH.value].apply(str) + '-' +
                                                               self.df[self.Columns.DAY.value].apply(str) + '-' +
                                                               self.df[self.Columns.YEAR.value].apply(str) + ' ' +
                                                               self.df[self.Columns.TIME.value])
        self.df.drop(self.df.columns[:4], axis=1, inplace=True)

        # Set datetime column as index
        self.df.set_index(pd.DatetimeIndex(self.df[self.Columns.DATE_TIME.value]), inplace=True)
        self.df.drop(self.Columns.DATE_TIME.value, axis=1, inplace=True)

        # Remove Smoke labels
        self.df[self.Columns.WEATHER_CONDITION.value] = np.where(
            self.df[self.Columns.WEATHER_CONDITION.value] == self.WEATHER_COND_SMOKE,
            np.nan, self.df[self.Columns.WEATHER_CONDITION.value])

        # Convert labels to ranked value
        for i, weather_cond in enumerate(self.WEATHER_COND_RANKED_LIST):
            self.df[self.Columns.WEATHER_CONDITION.value] = np.where(
                self.df[self.Columns.WEATHER_CONDITION.value] == weather_cond,
                str(i / (len(self.WEATHER_COND_RANKED_LIST) - 1)), self.df[self.Columns.WEATHER_CONDITION.value])

        self.df[self.Columns.WEATHER_CONDITION.value] = self.df[self.Columns.WEATHER_CONDITION.value].astype(float)
        self.df = self.df.resample('15T')
        self.df = self.df.interpolate(method='linear')
        # print(self.df.head(96).to_string())

    def normalize(self):
        # Get all unique weather condition values
        # weather_cond_col_list = self.df.time_weather.unique()

        # for weather_cond_col in weather_cond_col_list:
        #     self.df[weather_cond_col] = np.where(
        #         self.df[self.Columns.WEATHER_CONDITION.value] == weather_cond_col, 1, 0)

        self.df = (self.df - self.df.min()) / (self.df.max() - self.df.min())

        print(self.df.head(10).to_string())
