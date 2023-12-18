from src import db , login_manager
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import json

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)


class jsoncodedDict(db.TypeDecorator):
    impl = db.String

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    username = db.Column(db.String(50), unique= True)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    country = db.Column(db.String(50), unique= False)
    # state = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    zipcode = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(200), unique= False , default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name
    


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(30), unique=True, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(jsoncodedDict)

    def __repr__(self):
        return f'<CustomerOrder {self.invoice}>'
    
class Coupons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=True)
    user_id = db.Column(db.Integer, nullable=True) 

    def __init__(self, code=None, user_id=None):
        self.code = code
        self.user_id = user_id






