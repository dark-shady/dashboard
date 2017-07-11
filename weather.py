import requests
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

def get_weather():
    r = requests.get('https://api.darksky.net/forecast/{}/{},{}'.format(config['darksky']['api-key'],
                                                                        config['darksky']['latitude'],
                                                                        config['darksky']['longitude']))
    weather_data = r.json()

    weather_data['currently']['temperatureMin'] = weather_data['daily']['data'][0]['temperatureMin']
    weather_data['currently']['temperatureMax'] = weather_data['daily']['data'][0]['temperatureMax']

    return weather_data['currently'], weather_data['daily']['data'], weather_data['hourly']['data']


'''
first block:
weather_data['currently']
weather_data['daily']['data'][0]['temperatureMin']
weather_data['daily']['data'][0]['temperatureMax']

'''




'''
icons:


clear-night
partly-cloudy-day
rain



'''
