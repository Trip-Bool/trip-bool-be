import json
import os
import urllib.request
from flask import make_response

weather_key = os.environ.get("WEATHER_API_KEY")
timezone_key = os.environ.get("TIMEZONE_API_KEY")

def get_info(url):
    '''
    Given a url, this function makes a get request to the provided url, then converts the json recieved into a python dictionary. 
    '''
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return dict

def coordinates(location):
    '''
    Returs an object with latitude and lon keys of a given location. 
    '''
    location_key = os.environ.get("LOCATIONIQ_KEY")
    coordinates_url = f"https://us1.locationiq.com/v1/search?key={location_key}&q={location}&format=json"
    coordinates_dict = get_info(coordinates_url)
    coords = {
        "lat": coordinates_dict[0]["lat"],
        "lon": coordinates_dict[0]["lon"],
    }
    return make_response(coords, 200)



def current_weather(lat, lon):
    '''
    takes in lat and long and return an list of objects with the eight days of weather data. Data is a list of objects with a temp and weather attributes. 
    '''
    weather_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=imperial&appid={weather_key}'
    weather_info = get_info(weather_url)
    weather_data = []
    for day in weather_info["daily"]:
        weather_data.append({
            "temp": day["temp"]["day"],
            "weather": day["weather"],
        })
    dict_weather = {"data": weather_data}
    return make_response(dict_weather, 200)


def weather_time_machine(lat, lon, day):
    '''
    lat, lon, and day as parameters. Day should be one year before the trip day being used for the query. returns weather data as an object with a temp and weather parameters. 
    '''
    weather_url = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={day}&units=imperial&appid={weather_key}'
    weather_info = get_info(weather_url)
    history_data = {
        "temp": weather_info['data'][0]["temp"],
        "weather": weather_info['data'][0]["weather"],
    }
    return make_response(history_data, 200)


def timezone_adjust():
    pass
# http://api.timezonedb.com/v2.1/get-time-zone?key=BUAA5HGQEO7Y&format=json&by=position&lat=40.689247&lng=-74.044502


def get_time_zone(lat, lon, unix):
    timezone_url = f'http://api.timezonedb.com/v2.1/get-time-zone?key={timezone_key}&format=json&by=position&lat={lat}&lng={lon}&time={unix}'
    timezone_info = get_info(timezone_url)
    timezone_data = {
        "gmt_offset": timezone_info["gmtOffset"],
        "timestamp": timezone_info["timestamp"],
        "formatted": timezone_info["formatted"],
    }
    return make_response(timezone_data, 200)