from src import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Register(db.model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    country = db.Column(db.String(80), unique=False, nullable=False)
    state = db.Column(db.String(50), unique=False, nullable=False)
    city = db.Column(db.String(180), unique=False, nullable=False)
    zipcode  = db.Column(db.String(180), unique=False, nullable=False)

    profile = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')

    date_created = db.Column(db.DateTime , nullable=False , default=datetime.utcnow)

    
    def __repr__(self):
        return '<Register %r>' % self.name

