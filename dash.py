
from flask import render_template, Flask
import tv
import weather
import datetime
app = Flask(__name__)

@app.template_filter('format_date_US')
def format_date_US(unix_timestamp):
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
    return timestamp.strftime('%I:%M %p')

@app.template_filter('format_day')
def format_day(unix_timestamp):
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
    return timestamp.strftime('%A')

@app.route('/')
@app.route('/index')
@app.route('/tv')
def index():
    today, tomorrow, week = tv.tv_data()
    return render_template('tv.html',
                           today=today,
                           tomorrow=tomorrow,
                           week=week)

@app.route('/weather')
def display_weather():
    currently, daily, hourly = weather.get_weather()
    return render_template('weather.html',
                           currently=currently,
                           hourly=hourly,
                           daily=daily)
