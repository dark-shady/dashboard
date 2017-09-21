import requests
import json
import pendulum
import tvdb
import sqlite3

tvdb = tvdb.TVDB()

with open('config.json', 'r') as f:
    config = json.load(f)


def query_trakt(api_url):
    query_url = config['base_url'] + api_url
    headers = {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + config['access_token'],
              'trakt-api-version': config['trakt_api_version'],
              'trakt-api-key': config['client_id']
              }
    try:
        r = requests.get(query_url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        refresh_token()
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)

    return r.json()


def refresh_token():
    refresh_url = 'https://api.trakt.tv/oauth/token'
    json_data = {
                "refresh_token": config['refresh_token'],
                "client_id": config['client_id'],
                "client_secret": config['secret_id'],
                "redirect_uri": config['oauth_uri'],
                "grant_type": "refresh_token"
                }

    try:
        r = requests.post(refresh_url, json=json_data)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        authorize()
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)

    update_config(r.json())


def authorize():
    pass

def update_config(new_config_values):
    for key in new_config_values:
        config[key] = new_config_values[key]

    with open('config.json', 'w') as f:
        json.dump(config, f)

def get_banner(tvdb_id):
    banners = tvdb.show_banners(tvdb_id)['data']

    highest_rating, highest_rated = 0.0, ""

    for key in banners:
        if key['ratingsInfo']['average'] >= highest_rating:
            highest_rating = key['ratingsInfo']['average']
            highest_rated = key['fileName']
    return 'http://thetvdb.com/banners/' +highest_rated

def parse_data(data):
    today, tomorrow, week = [], [], []

    for i, item in enumerate(data):
        dt = pendulum.parse(data[i]['first_aired'])
        dt = dt.in_tz('America/New_York')
        item['first_aired'] = dt.format("%a %I:%M %p")

        item['bannerpath'] = get_banner(item['show']['ids']['tvdb'])

        if dt.is_today():
            today.append(item)
        elif dt.is_tomorrow():
            tomorrow.append(item)
        elif dt.is_future():
            week.append(item)

    return today, tomorrow, week


def tv_data():
    return parse_data(query_trakt("/calendars/my/shows"))
