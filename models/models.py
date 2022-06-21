from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TripModel(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    date_start = db.Column(db.DateTime())
    date_end = db.Column(db.DateTime())
    location = db.Column(db.String(80))
    
    def __repr__(self):
        return f"Name:{self.name}, Date Start:{self.date_start}, Date End: {self.date_end}, Location:{self.location}"