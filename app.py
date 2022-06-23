from flask import Flask, redirect, request, jsonify, make_response, render_template, url_for, session
from flask_migrate import Migrate
from models.models import db, TripModel
import os
import datetime
import json
from urllib.parse import quote_plus, urlencode
from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth
from weather_parse import current_weather, weather_time_machine, coordinates
import requests
from flask_cors import CORS


# ENV Setup
username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
db_url = os.environ.get('DB_URL')
db_name = os.environ.get('DB_NAME')
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
CORS(app)

# OAuth Setup
app.secret_key = os.environ.get("APP_SECRET_KEY")
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id = os.environ.get("AUTH0_CLIENT_ID"),
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{db_url}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_table():
    db.create_all()

# Database Routes
@app.route('/data/create', methods=["POST"])
def create():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        location = request.form['location']
        start_datetime = datetime.datetime.fromisoformat(start_date)
        end_datetime = datetime.datetime.fromisoformat(end_date)
        start_unix = datetime.datetime.timestamp(start_datetime)
        end_unix = datetime.datetime.timestamp(end_datetime)
        trip = TripModel(name=name, start_date=start_unix, end_date=end_unix, location=location)
        db.session.add(trip)
        db.session.commit()
        return make_response("", 201)



@app.route('/data')
def retrieve_list():
    trips = TripModel.query.all()
    data = {}
    for trip in trips:
        item = {
            "name": trip.name,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "location": trip.location
        }
        data[f'{trip.id}'] = item
    return make_response(data, 200)


@app.route('/data/<int:id>')
def retrieve_trip(id):
    trip = TripModel.query.filter_by(id=id).first()
    if trip:
        data = {
            "name": trip.name,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "location": trip.location
        }
        return make_response(data, 200)
    return make_response("", 204)

@app.route('/data/<int:id>/update', methods=['GET','POST'])
def update(id):
    trip = TripModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if trip:
            db.session.delete(trip)
            db.session.commit()
            name = request.form['name']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            location = request.form['location']
            start_datetime = datetime.datetime.fromisoformat(start_date)
            end_datetime = datetime.datetime.fromisoformat(end_date)
            start_unix = datetime.datetime.timestamp(start_datetime)
            end_unix = datetime.datetime.timestamp(end_datetime)
            trip = TripModel(name=name, start_date=start_unix, end_date=end_unix, location=location)
            db.session.add(trip)
            db.session.commit()
            return make_response("", 201)
        return make_response("", 204)

    return make_response(trip, 200)

@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    trip = TripModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if trip:
            db.session.delete(trip)
            db.session.commit()
            return make_response("", 410)
        return make_response('', 404)
    
    return make_response(trip, 200)

@app.route('/data/<string:name>')
def get_by_name(name):
    trips = TripModel.query.filter_by(name=name).all()
    data = {}
    if trips:
        for trip in trips:
            item = {
                "name": trip.name,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "location": trip.location
            }
            data[f'{trip.id}'] = item
    return make_response(data, 200)

@app.route('/yelp/restaurants/<latitude>/<longitude>/<string:price>')
def yelp_restaurant_api_call(latitude,longitude,price):
    url = f'https://api.yelp.com/v3/businesses/search?term=restaurants&radius=16093&limit=10&sort_by=rating&price={price}&latitude={latitude}&longitude={longitude}'
    yelp_key = os.environ.get("YELP_API_KEY")
    headers = {"Authorization": f"Bearer {yelp_key}"}
    response = requests.get(url, headers=headers)
    return make_response(response.json(), 200)

@app.route('/yelp/outdoors/<latitude>/<longitude>')
def yelp_outdoors_api_call(latitude,longitude):
    url = f'https://api.yelp.com/v3/businesses/search?term=outdoor activities&radius=16093&limit=10&sort_by=rating&latitude={latitude}&longitude={longitude}'
    yelp_key = os.environ.get("YELP_API_KEY")
    headers = {"Authorization": f"Bearer {yelp_key}"}
    response = requests.get(url, headers=headers)
    return make_response(response.json(), 200)

@app.route('/yelp/hotels/<latitude>/<longitude>/<string:price>')
def yelp_hotel_api_call(latitude,longitude,price):
    url = f'https://api.yelp.com/v3/businesses/search?categories=hotels&radius=16093&limit=10&sort_by=rating&price={price}&latitude={latitude}&longitude={longitude}'
    yelp_key = os.environ.get("YELP_API_KEY")
    headers = {"Authorization": f"Bearer {yelp_key}"}
    response = requests.get(url, headers=headers)
    return make_response(response.json(), 200)

# Home Route
@app.route("/")
def index():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


# Weather Routes


@app.route("/weather/<int:id>")
def get_weather_by_id(id):
    response = retrieve_trip(id)  # might need to replace with GET request w/ url route
    trip_object = response.json
    location = trip_object["location"]
    start_date = trip_object["start_date"]
    end_date = trip_object["end_date"]
    weather_data = get_trip_weather(location, start_date, end_date)
    if weather_data.status_code == 400:
        return make_response("Invalid Start Date, You likely chose a date in the past.", 400)
    trip_weather = weather_data.json
    return make_response(trip_weather, 200)



@app.route("/weather/<string:location>/<int:start_date>/<int:end_date>")
def get_trip_weather(location, start_date, end_date):
    """
    Function takes a trip's location, start and end dates.
    Returns a collection of weather data for the trip's duration.

    Helper functions
    ----------------
    :get_forecast(): collects forecast data for given date range
    :get_historic(): collects historic data for given date range
    :get_both(): collects mix of forecast and historic data

    Arguments
    ---------
    :location: string
    :start_date: Unix 10-digit (float)
    :end_date: Unix 10-digit (float)

    Returns
    -------
    :data_collections: list holding the two following dict objects
    :forecast_weather: dict holding weather data for dates within next 7 days
    :historic_weather: dict holding weather data for dates beyond next 7 days
    """
    start_date = round(start_date)
    end_date = round(end_date)
    coords = coordinates(location)
    date_today = normalize_current_time()
    days_from_today = round((start_date - date_today) / 86400)
    if days_from_today < 0:
        return make_response("Invalid Start Date, You likely chose a date in the past.", 400)
    boundary = add_time_to_stamp(date_today, 7)
    forecast_weather = []
    historic_weather = []
    all_weather = {}
    date_list = []

    date_marker = start_date
    while date_marker <= end_date:
        date_list.append(date_marker)
        date_marker = add_time_to_stamp(date_marker, 1)

    if start_date >= boundary:
        get_historic(coords, date_list, historic_weather)
    elif end_date >= boundary:
        get_both(coords, days_from_today, boundary, date_list, forecast_weather, historic_weather)
    else:
        get_forecast(coords, days_from_today, date_list, forecast_weather)
    all_weather["destination"] = location.title()
    all_weather["forecast_weather"] = forecast_weather
    all_weather["historic_weather"] = historic_weather
    return make_response(all_weather, 200)


def get_forecast(coords, days_from_today, dates, forecasts=[]):
    """
    Function takes a list of dates and an empty dictionary.
    Directs one API call for forecast weather data, and parses through it.
    Extracts relevant data for each date in date_list and adds to dictionary.

    Arguments
    ---------
    :dates: list of dates passed in from get_trip_weather()
    :forecasts: empty dictionary passed in from get_trip_weather()
    """
    coords_response = coords.json
    api_result = current_weather(coords_response["lat"], coords_response["lon"])
    api_response = api_result.json
    index = days_from_today
    # for date in dates:
    #     date_keys.append(str(date))
    # forecasts["dates"] = date_keys
    for date in dates:
        date_weather = api_response["data"][index]
        forecasts.append(date_weather)
        date_weather["date"] = str(date)
        index += 1
    return


def get_historic(coords, dates, historics=[]):
    """
    Function takes a list of dates and an empty dictionary.
    Iterates through dates, directs an API call for historic weather data for each.
    Extracts relevant data and adds to dictionary.

    Arguments
    ---------
    :dates: list of dates passed in from get_trip_weather()
    :forecasts: empty dictionary passed in from get_trip_weather()
    """
    lat = coords.json["lat"]
    lon = coords.json["lon"]
    for date in dates:
        last_year_date = add_time_to_stamp(date, -365)
        api_response = weather_time_machine(lat, lon, last_year_date)
        date_weather = api_response.json
        date_weather["date"] = str(date)
        historics.append(date_weather)
    return


def get_both(coords, from_today, boundary, dates, forecasts=[], historics=[]):
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


def normalize_current_time():
    current_datetime = datetime.datetime.now()
    current_dt_str = str(current_datetime)
    num_hrs = int(current_dt_str[11:13])
    num_mins = int(current_dt_str[14:16])
    num_secs = int(current_dt_str[17:19])
    today_total_secs = (num_hrs * 3600) + (num_mins * 60) + num_secs
    current_timestamp = round(datetime.datetime.timestamp(current_datetime))
    today_normalized = current_timestamp - today_total_secs
    return today_normalized


# Helpful testing functions that can eventually be removed:


def convert_from_timestamp(unix):
    date = datetime.datetime.fromtimestamp(unix)
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




# Auth0 Routes
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        'https://'+os.environ.get("AUTH0_DOMAIN")+'/v2/logout?'+urlencode(
            {
                'returnTo': url_for("index", _external=True),
                'client_id': os.environ.get('AUTH0_CLIENT_ID'),
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run(debug=True)


"""

"""