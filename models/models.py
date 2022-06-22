from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TripModel(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    start_date = db.Column(db.Float())
    end_date = db.Column(db.Float())
    location = db.Column(db.String(80))
    
    def __repr__(self):
        return f"Name:{self.name}, Date Start:{self.start_date}, Date End: {self.end_date}, Location:{self.location}"