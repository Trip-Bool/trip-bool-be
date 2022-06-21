from flask import Flask, redirect, request, jsonify, make_response
from flask_migrate import Migrate
from models.models import db, TripModel
import os

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
        length = request.form['length']
        location = request.form['location']
        trip = TripModel(name=name,length=length,location=location)
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
            "length": trip.length,
            "location": trip.location
        }
        data[f'{trip.id}'] = item
    return make_response(data, 200)

@app.route('/data/<int:id>')
def retrive_trip(id):
    trip = TripModel.query.filter_by(id=id).first()
    if trip:
        data = {
            "name": trip.name,
            "length": trip.length,
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
            length = request.form['length']
            location = request.form['location']
            trip = TripModel(id=id, name=name,length=length,location=location)
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
    
    return jsonify(trip)


@app.route("/")
def index():
    return redirect("/data")

if __name__ == "__main__":
    app.run(debug=True)
