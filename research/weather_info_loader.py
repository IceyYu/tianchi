import os
import pickle
from data_loader import DataLoader

files_key = filter(lambda x: x != 'simao', os.listdir('city_weather'))
files_value = map(lambda x: '/city_weather/'+x, files_key)
weather_value = [DataLoader.dump_data_frame(file_name, columns=['date', 'high', 'low', 'rainy', 'wind_direction',
                                                                'wind_force']) for file_name in files_value]
weather = dict(zip(files_key, weather_value))
pickle.dump(weather, open('weather_info', 'w+'))
