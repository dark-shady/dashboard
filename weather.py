import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

CARDINAL = ["N","NE","E","SE","S","SW","W","NW","N"]


def get_weather():
    r = requests.get('https://api.darksky.net/forecast/{}/{},{}'.format(config['darksky']['api-key'],
                                                                        config['darksky']['latitude'],
                                                                        config['darksky']['longitude']))
    weather_data = r.json()

    #add temp min, max to currently for ease
    weather_data['currently']['temperatureMin'] = weather_data['daily']['data'][0]['temperatureMin']
    weather_data['currently']['temperatureMax'] = weather_data['daily']['data'][0]['temperatureMax']

    #Humidity/Precip from 0-1 to 0-100
    weather_data['currently']['humidity'] *= 100
    weather_data['currently']['precipProbability'] *=100
    #MOON phase from 0-1 to 0-24.
    weather_data['daily']['data'][0]['moonPhase'] = int(((weather_data['daily']['data'][0]['moonPhase'])) * (26))

    #Day timestamp to Day


    #Wind Direction
    weather_data['currently']['windBearing'] = CARDINAL[int(weather_data['currently']['windBearing'] / 45)]


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
