from MMDATrafficData import MMDATrafficData
from WeatherForYouData import WeatherForYou

WEATHER_DATA_PATH = 'C:\\Users\Gelo\Documents\Gelo103097\DLSU Files\THESIS\data\weather\\'
WEATHER_DATA_WEATHERFORYOU_2015_MANILA_PATH = WEATHER_DATA_PATH + '\\weatherforyou 2015\\'
WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH = WEATHER_DATA_PATH + 'weatherforyou_normalized_manila_2015.csv'
WEATHER_DATA_TIMEANDDATE_2015_MANILA_PATH = WEATHER_DATA_PATH + 'timeanddate 2015\Manila\\'

TRAFFIC_DATA_PATH = 'C:\\Users\Gelo\Documents\Gelo103097\DLSU Files\THESIS\data\\traffic\\'
TRAFFIC_DATA_LINE_NAME_PATH = TRAFFIC_DATA_PATH + 'line_names.csv'
TRAFFIC_DATA_LINE_STATION_PATH = TRAFFIC_DATA_PATH + 'line_stations.csv'
TRAFFIC_DATA_2015_PATH = TRAFFIC_DATA_PATH + 'status_collated_2015.csv'


# weatherforyou = WeatherForYou(WEATHER_DATA_WEATHERFORYOU_2015_MANILA_PATH + '{month:02d}-{year}.csv', 2015)
# weatherforyou.save(WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH)

mmda_traffic = MMDATrafficData(TRAFFIC_DATA_LINE_NAME_PATH, TRAFFIC_DATA_LINE_STATION_PATH, TRAFFIC_DATA_2015_PATH,
                               ['ESPAÑA', 'ROXAS BLVD.'], ['Taft Ave.', 'Magsaysay Ave', 'Quezon Ave.'])
