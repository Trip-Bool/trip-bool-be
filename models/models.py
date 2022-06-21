from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TripModel(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    length = db.Column(db.Integer())
    location = db.Column(db.String(80))
    
    def __repr__(self):
        return f"Name:{self.name}, Length:{self.length}, Location:{self.location}"