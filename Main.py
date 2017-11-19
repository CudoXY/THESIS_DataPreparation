from MMDATrafficData import MMDATrafficData
from MergeMMDAWeatherForYou import MergeMMDAWeatherForYou
from MergeMMDAWWO import MergeMMDAWWO
from WeatherForYouData import WeatherForYou
from WWOData import WWOData

import pandas as pd
import numpy as np
import glob, os

DATA_PATH = 'C:\\Users\\user\\Documents\Gelo103097\DLSU Files\THESIS\data\\'

WEATHER_DATA_PATH = DATA_PATH + 'weather\\'

WEATHER_DATA_WEATHERFORYOU_2015_MANILA_PATH = WEATHER_DATA_PATH + '\\weatherforyou 2015\\'
WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH = WEATHER_DATA_PATH + 'weatherforyou_normalized_manila_2015.csv'

WEATHER_DATA_WWO_2015_MANILA_PATH = WEATHER_DATA_PATH + '\\worldweatheronline 2015\\csv\\'
WEATHER_DATA_WWO_2015_MANILA_SAVE_PATH = WEATHER_DATA_PATH + 'worldweatheronline_normalized_manila_2015.csv'

WEATHER_DATA_TIMEANDDATE_2015_MANILA_PATH = WEATHER_DATA_PATH + 'timeanddate 2015\Manila\\'

TRAFFIC_DATA_PATH = DATA_PATH + 'traffic\\'

TRAFFIC_DATA_LINE_NAME_PATH = TRAFFIC_DATA_PATH + 'line_names.csv'
TRAFFIC_DATA_LINE_STATION_PATH = TRAFFIC_DATA_PATH + 'line_stations.csv'
TRAFFIC_DATA_2015_PATH = TRAFFIC_DATA_PATH + 'status_collated_2015.csv'
TRAFFIC_DATA_2015_MANILA_SAVE_PATH = TRAFFIC_DATA_PATH + 'mmda_normalized_manila_2015.csv'

MERGED_MMDA_WEATHERFORYOU_2015_MANILA_SAVE_PATH = DATA_PATH + 'merged_mmda_weatherforyou_manila_2015.csv'
MERGED_MMDA_WEATHERFORYOU_2015_FORMATTED_SAVE_PATH = DATA_PATH + 'merged_mmda_weatherforyou_{label}_2015.csv'

MERGED_MMDA_WWO_2015_MANILA_SAVE_PATH = DATA_PATH + 'merged_mmda_wwo_manila_2015.csv'
MERGED_MMDA_WWO_2015_FORMATTED_SAVE_PATH = DATA_PATH + 'merged_mmda_wwo_{label}_2015.csv'

# weatherforyou = WeatherForYou(WEATHER_DATA_WEATHERFORYOU_2015_MANILA_PATH + '{month:02d}-{year}.csv', 2015)
# weatherforyou.save(WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH)

# mmda_traffic = MMDATrafficData(TRAFFIC_DATA_LINE_NAME_PATH, TRAFFIC_DATA_LINE_STATION_PATH, TRAFFIC_DATA_2015_PATH,
#                                ['ESPAÑA', 'ROXAS BLVD.'], ['Taft Ave.', 'Magsaysay Ave', 'Quezon Ave.'])
# mmda_traffic.save(TRAFFIC_DATA_2015_MANILA_SAVE_PATH)

# merge_mmda_weatherforyou = MergeMMDAWeatherForYou(TRAFFIC_DATA_2015_MANILA_SAVE_PATH,
#                                                   WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH)
# merge_mmda_weatherforyou.save(MERGED_MMDA_WEATHERFORYOU_2015_MANILA_SAVE_PATH)
# merge_mmda_weatherforyou.save_formatted(MERGED_MMDA_WEATHERFORYOU_2015_FORMATTED_SAVE_PATH,
#                                         merge_mmda_weatherforyou.SaveMode.BY_STATION)

# worldweatheronline = WorldWeatherOnlineData(WEATHER_DATA_WORLDWEATHERONLINE_2015_MANILA_PATH +
#                                             'manila-{month:02d}-{year}.json', 2015)





# WWO

# wwo = WWOData(WEATHER_DATA_WWO_2015_MANILA_PATH + 'manila-{month:02d}-{year}.csv', 2015)
# wwo.save(WEATHER_DATA_WWO_2015_MANILA_SAVE_PATH)

mmda_traffic = MMDATrafficData(TRAFFIC_DATA_LINE_NAME_PATH, TRAFFIC_DATA_LINE_STATION_PATH, TRAFFIC_DATA_2015_PATH,
                               ['ESPAÑA', 'ROXAS BLVD.'], ['Taft Ave.', 'Magsaysay Ave', 'Quezon Ave.'])
mmda_traffic.save(TRAFFIC_DATA_2015_MANILA_SAVE_PATH)

merge_mmda_wwo = MergeMMDAWWO(TRAFFIC_DATA_2015_MANILA_SAVE_PATH,
                                                  WEATHER_DATA_WWO_2015_MANILA_SAVE_PATH)
merge_mmda_wwo.save(MERGED_MMDA_WWO_2015_MANILA_SAVE_PATH)
merge_mmda_wwo.save_formatted(MERGED_MMDA_WWO_2015_FORMATTED_SAVE_PATH,
                                        merge_mmda_wwo.SaveMode.BY_STATION)















# CORRELATION
# ave_cor_df = pd.DataFrame()
#
# os.chdir(DATA_PATH)
# for file in glob.glob("merged_mmda_weatherforyou_Coastal Road_2015.csv"):
#     df = pd.read_csv(file, sep=',\s,', delimiter=',',
#                      skipinitialspace=True)
#     df.drop(df.columns[:2], axis=1, inplace=True)
#     df.drop(df.columns[2:4], axis=1, inplace=True)
#
#     cor = np.corrcoef(df[df.columns[0:]].T)
#
#     cor_df = pd.DataFrame(cor)
#     cor_df.columns = ['statusN', 'statusS', 'time_weather', 'time_temp', 'time_dewpt', 'time_hum', 'time_pressure',
#                       'time_winds']
#
#     for i in range(0, len(cor_df.columns)):
#         cor_df.rename(index={i: cor_df.columns[i]}, inplace=True)
#
#     # concatenate them
#     if len(ave_cor_df) <= 0:
#         ave_cor_df = cor_df
#         continue
#
#     ave_cor_df = pd.concat((ave_cor_df, cor_df), axis=1)
#     ave_cor_df = ave_cor_df.stack().groupby(level=[0, 1]).std().unstack()
#
# ave_cor_df = ave_cor_df[['statusN', 'statusS', 'time_weather', 'time_temp', 'time_dewpt', 'time_hum', 'time_pressure',
#                       'time_winds']]
#
# print(ave_cor_df.to_string())
