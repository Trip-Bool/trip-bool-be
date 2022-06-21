from flask import Flask, redirect, request, jsonify, make_response
from flask_migrate import Migrate
from models.models import db, TripModel
import os
import datetime
import urllib.request, json


# Date Start and Date End Unix Conversions:
    # "start_unix": datetime.datetime.timestamp(trip.date_start)
    # "end_unix": datetime.datetime.timestamp(trip.date_end)


username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
db_url = os.environ.get('DB_URL')
db_name = os.environ.get('DB_NAME')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{db_url}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/data/create', methods=["POST"])
def create():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        location = request.form['location']
        start_datetime = datetime.datetime.fromisoformat(start_date)
        end_datetime = datetime.datetime.fromisoformat(end_date)
        trip = TripModel(name=name, date_start=start_datetime, date_end=end_datetime, location=location)
        db.session.add(trip)
        db.session.commit()
        return make_response("", 201)

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
    coordinates_url = f"https://us1.locationiq.com/v1/search?key=YOUR_ACCESS_TOKEN&q={location}&format=json"
    coordinates_dict = get_info(coordinates_url)
    return {
        "lat": coordinates_dict["lat"],
        "lon": coordinates_dict["lon"],
    }

def current_weather(lat, lon):
    '''
    takes in lat and long and return an list of objects with the eight days of weather data. Data is a list of objects with a temp and weather attributes. 
    '''
    weather_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid=APIkey'
    weather_info = get_info(weather_url)
    weather_data = []
    for day in weather_info["daily"]:
        weather_data.append({
            "temp": day["temp"]["day"],
            "weather": day["weather"],
        })
    return weather_data


def weather_time_machine(lat, lon, day):
    '''
    lat, lon, and day as parameters. Day should be one year before the trip day being used for the query. returns weather data as an object with a temp and weather parameters. 
    '''
    weather_url = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={day}&appid=APIkey'
    weather_info = get_info(weather_url)
    return {
        "temp": weather_info['data'][0]["temp"],
        "weather": weather_info['data'][0]["weather"],
    }


# def weather_data_retreval_parseing(trip):
#     coordinates_url = "https://us1.locationiq.com/v1/search?key=YOUR_ACCESS_TOKEN&q={trip.location}&format=json"
#     coordinates_dict = get_info(coordinates_url)

#     if "dates are more than 8 days away from today":
#         weather_data = []
#         for every day:
#             # time being exactly one year befre that day
#             weather_url = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={coordinates_dict["lat"]}&lon={coordinates_dict["lon"]}&dt={time}&appid=API key'
#             weather_info = get_info(weather_url)
#             weather_data.append({
#                 "temp": weather_info['data'][0]["temp"],
#                 "weather": weather_info['data'][0]["weather"],
#             })
#     else:
#         weather_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={coordinates_dict["lat"]}&lon={coordinates_dict["lon"]}&exclude={part}&appid=API key'
#         weather_info = get_info(weather_url)
#         for day in weather_info["daily"]:
#             weather_data.append({
#                 "temp": day["temp"]["day"],
#                 "weather": day["weather"],
#             })

@app.route('/data')
def retrieve_list():
    trips = TripModel.query.all()
    data = {}
    for trip in trips:
        item = {
            "name": trip.name,
            "date_start": trip.date_start,
            "date_end": trip.date_end,
            "location": trip.location,
        }
        data[f'{trip.id}'] = item
    return make_response(data, 200)

@app.route('/data/<int:id>')
def retrive_trip(id):
    trip = TripModel.query.filter_by(id=id).first()
    if trip:
        data = {
            "name": trip.name,
            "date_start": trip.date_start,
            "date_end": trip.date_end,
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
            trip = TripModel(name=name, date_start=start_datetime, date_end=end_datetime, location=location)
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


@app.route("/")
def index():
    return redirect("/data")

if __name__ == "__main__":
    app.run(debug=True)
