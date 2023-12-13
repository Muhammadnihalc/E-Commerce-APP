from src import db , login_manager
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import json

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)


class jsoncodedDict(db.TypeDecorator):
    impl = db.test

    def set_value(self, value , dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

class Register(db.model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=False, nullable=False)
    f_name = db.Column(db.String(50), unique=False)
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
    

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(30), unique=True, nullable=False)
    status = db.Column(db.String(30), unique=True, nullable=False , default='pending')
    customer_id = db.Column(db.Integer, unique=False nullable=False)
    customer_id = db.Column(db.DateTime, default='datetime.utcnow', nullable=False)
    orders = db.Column(db.String(30), unique=True, nullable=False)

