from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

import pandas as pd
import numpy as np

WEATHER_DATA_PATH = 'C:\\Users\Gelo\Documents\Gelo103097\DLSU Files\THESIS\data\weather\\'
WEATHER_DATA_WEATHERFORYOU_2015_MANILA_PATH = WEATHER_DATA_PATH + '\\weatherforyou 2015\\'
WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH = WEATHER_DATA_PATH + 'weatherforyou_normalized_manila_2015.csv'
WEATHER_DATA_TIMEANDDATE_2015_MANILA_PATH = WEATHER_DATA_PATH + '\\timeanddate 2015\Manila\\'

TRAFFIC_DATA_PATH = 'C:\\Users\Gelo\Documents\Gelo103097\DLSU Files\THESIS\data\traffic\\'


class WeatherDataSource(Enum):
    WEATHERFORYOU = 1
    TIMEANDDATE = 2


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


class WeatherForYou(WeatherData):
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



weatherforyou = WeatherForYou(WEATHER_DATA_WEATHERFORYOU_2015_MANILA_PATH + '{month:02d}-{year}.csv', 2015)
weatherforyou.save(WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH)
