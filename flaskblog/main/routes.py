import os, requests
from math import ceil
from flask import Blueprint, render_template, request
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    apiKey = os.environ.get("WEATHER_API_KEY")
    posts = Post.query.all()
    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/group?id=5809844,5746545,5419384&appid={apiKey}')
    responseJson = response.json()
    cityList = responseJson['list']
    seattleKelvin = cityList[0]['main']['temp']
    seattleFahrenheit = kelvinToFahrenheit(seattleKelvin)
    portlandKelvin = cityList[1]['main']['temp']
    portlandFahrenheit = kelvinToFahrenheit(portlandKelvin)
    denverKelvin = cityList[0]['main']['temp']
    denverFahrenheit = kelvinToFahrenheit(denverKelvin)
    return render_template('home.html', posts=posts, title='Home', seattleTemp=seattleFahrenheit, portlandTemp=portlandFahrenheit, denverTemp=denverFahrenheit)


def kelvinToFahrenheit(temp):
    return ceil((temp - 273.15) * 1.8 + 32)


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/resume')
def resume():
    return render_template('resume.html', title="Resume")
