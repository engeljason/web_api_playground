
import requests
from api_keys import wkey
import os, os.path
import errno
from scipy.stats import linregress
from matplotlib import pyplot as plt

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))

    return open(path, 'w', encoding = "UTF-16")
###


def make_graph(x, y, x_label = None, y_label = None, title = None, linreg = False):
    slope, int, r, p, std_err = linregress(x = x, y = y)
    fit = slope * x + int
    plt.scatter(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if linreg:
        plt.plot(x,fit,"r--")
        plt.legend(['y={:.2f}x+{:.2f}'.format(slope,int)])
        print(f'r = {r:.5f}')
    return plt


def request_city(city : str):
    url = "http://api.openweathermap.org/data/2.5/weather"

    q = city
    appid = wkey
    mode = "json"
    units = "imperial"

    params = {
        "q" : q,
        "appid" : appid,
        "mode" : mode,
        "units" : units
    }

    return requests.get(url=url, params=params)

def make_row(json):
    max_temp = json["main"]["temp_max"]
    temperature = json["main"]["temp"]
    humidity = json["main"]["humidity"]
    cloudiness = json["clouds"]["all"]
    wind_speed = json["wind"]["speed"]
    date = json["dt"]
    lat = json["coord"]["lat"]
    lng = json["coord"]["lon"]
    name = json["name"]
    country = json["sys"]["country"]

    row = {}
    for variable in ["name", "country", "lat", "lng", "max_temp", "temperature", "humidity",
            "cloudiness", "wind_speed", "date"]:
        row[variable] = eval(variable)

    return row


###
#   JSON schema for OpenWeather API request
###
#     {
#   "coord": {
#     "lon": -122.08,
#     "lat": 37.39
#   },
#   "weather": [
#     {
#       "id": 800,
#       "main": "Clear",
#       "description": "clear sky",
#       "icon": "01d"
#     }
#   ],
#   "base": "stations",
#   "main": {
#     "temp": 282.55,
#     "feels_like": 281.86,
#     "temp_min": 280.37,
#     "temp_max": 284.26,
#     "pressure": 1023,
#     "humidity": 100
#   },
#   "visibility": 16093,
#   "wind": {
#     "speed": 1.5,
#     "deg": 350
#   },
#   "clouds": {
#     "all": 1
#   },
#   "dt": 1560350645,
#   "sys": {
#     "type": 1,
#     "id": 5122,
#     "message": 0.0139,
#     "country": "US",
#     "sunrise": 1560343627,
#     "sunset": 1560396563
#   },
#   "timezone": -25200,
#   "id": 420006353,
#   "name": "Mountain View",
#   "cod": 200
#   }                         
