
from flask import render_template, Flask
import tv
import weather
app = Flask(__name__)


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
