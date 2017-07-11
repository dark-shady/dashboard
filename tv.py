import trakt.calendar
import pendulum
import tvdb
import sqlite3

tvdb = tvdb.TVDB()

def get_banner(tvdb_id):
    banners = tvdb.show_banners(tvdb_id)['data']

    highest_rating, highest_rated = 0.0, None

    for key in banners:
        if key['ratingsInfo']['average'] > highest_rating:
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
    Cal_data = trakt.calendar.MyShowCalendar(days=8).data
    return parse_data(Cal_data)
