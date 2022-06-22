from datetime import datetime
import json
from app import current_weather, weather_time_machine, coordinates


def get_trip_weather(location, start_date, end_date):
    """
    Function takes a trip's start and end dates.
    Returns a collection of weather data for the trip's duration.

    Helper functions
    ----------------
    :get_forecast(): collects forecast data for given date range
    :get_historic(): collects historic data for given date range
    :get_both(): collects mix of forecast and historic data

    Arguments
    ---------
    :start_date: 10-digit Unix timestamp
    :end_date: 10-digit Unix timestamp

    Returns
    -------
    :data_collections: list holding the two following dict objects
    :forecast_weather: dict holding weather data for dates within next 7 days
    :historic_weather: dict holding weather data for dates beyond next 7 days
    """
    coords = coordinates(location)
    date_today = datetime.now()
    current = round(datetime.timestamp(date_today))
    days_from_today = round((start_date - current) / 86400)
    boundary = add_time_to_stamp(current, 7)
    forecast_weather = {}
    historic_weather = {}
    date_list = []

    date_marker = start_date
    while date_marker <= boundary:
        date_list.append(date_marker)
        date_marker = add_time_to_stamp(date_marker, 1)

    if start_date >= boundary:
        get_historic(coords, date_list, historic_weather)
    elif end_date >= boundary:
        get_both(coords, days_from_today, boundary, date_list, forecast_weather, historic_weather)
    else:
        get_forecast(coords, days_from_today, date_list, forecast_weather)

    data_collections = [forecast_weather, historic_weather]
    return data_collections


def get_forecast(coords, days_from_today, dates, forecasts={}):
    """
    Function takes a list of dates and an empty dictionary.
    Directs one API call for forecast weather data, and parses through it.
    Extracts relevant data for each date in date_list and adds to dictionary.

    Arguments
    ---------
    :dates: list of dates passed in from get_trip_weather()
    :forecasts: empty dictionary passed in from get_trip_weather()
    """
    api_result = current_weather(coords["lat"], coords["lon"])
    date_keys = []
    index = days_from_today
    for date in dates:
        date_keys.append(date)
    forecasts["dates"] = date_keys
    for date in dates:
        date_weather = api_result["data"][index]
        forecasts[date] = date_weather
        index += 1
    return


def get_historic(coords, dates, historics={}):
    """
    Function takes a list of dates and an empty dictionary.
    Iterates through dates, directs an API call for historic weather data for each.
    Extracts relevant data and adds to dictionary.

    Arguments
    ---------
    :dates: list of dates passed in from get_trip_weather()
    :forecasts: empty dictionary passed in from get_trip_weather()
    """
    historics["dates"] = dates
    lat = coords["lat"]
    lon = coords["lon"]
    for date in dates:
        last_year_date = add_time_to_stamp(date, -365)
        date_weather = weather_time_machine(lat, lon, last_year_date)
        historics[date] = date_weather
    return


def get_both(coords, from_today, boundary, dates, forecasts={}, historics={}):
    """
    docstring
    """
    forecast_dates = []
    historic_dates = []
    for date in dates:
        if date >= boundary:
            historic_dates.append(date)
        else:
            forecast_dates.append(date)
    get_historic(coords, historic_dates, historics)
    get_forecast(coords, from_today, forecast_dates, forecasts)
    return


def add_time_to_stamp(unix, num_days):
    time_add = num_days * 86400
    return unix + time_add


# Helpful testing functions that can eventually be removed:


def convert_from_timestamp(unix):
    date = datetime.fromtimestamp(unix)
    return date


def json_test(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data


def kelvin_to_fahrenheit(kelvin_temp):
    fahrenheit = (kelvin_temp - 273.15) * 9/5 + 32
    return fahrenheit


def render_test(collection):
    forecast_weather = collection[0]
    date_keys = forecast_weather['dates']
    days_of_week = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday',
    ]
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December',
    ]
    for date in date_keys:
        normal_date = convert_from_timestamp(date)
        day_of_week_index = normal_date.weekday()
        weekday = days_of_week[day_of_week_index]
        date_string = str(normal_date)
        month_index = int(date_string[5:7])
        month = months[month_index]
        day_of_month = date_string[8:10]
        year = date_string[0:4]
        kelvin = forecast_weather[date]["temp"]
        temp = round(kelvin_to_fahrenheit(kelvin))
        description = forecast_weather[date]["weather"][0]["description"]
        msg = f"{weekday} {month} {day_of_month}, {year} will be {temp}°, {description}"
        print(msg)


