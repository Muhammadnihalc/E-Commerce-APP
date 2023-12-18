from src import db

from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')

    # Relationship with orders
    orders = relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Other fields related to the order
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)




    def __repr__(self):
        return '<User %r>' % self.username
    
