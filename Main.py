from WeatherForYou import WeatherForYou

WEATHER_DATA_PATH = 'C:\\Users\Gelo\Documents\Gelo103097\DLSU Files\THESIS\data\weather\\'
WEATHER_DATA_WEATHERFORYOU_2015_MANILA_PATH = WEATHER_DATA_PATH + '\\weatherforyou 2015\\'
WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH = WEATHER_DATA_PATH + 'weatherforyou_normalized_manila_2015.csv'
WEATHER_DATA_TIMEANDDATE_2015_MANILA_PATH = WEATHER_DATA_PATH + '\\timeanddate 2015\Manila\\'

TRAFFIC_DATA_PATH = 'C:\\Users\Gelo\Documents\Gelo103097\DLSU Files\THESIS\data\traffic\\'


weatherforyou = WeatherForYou(WEATHER_DATA_WEATHERFORYOU_2015_MANILA_PATH + '{month:02d}-{year}.csv', 2015)
weatherforyou.save(WEATHER_DATA_WEATHERFORYOU_2015_MANILA_SAVE_PATH)
