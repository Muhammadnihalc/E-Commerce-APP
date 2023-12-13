from src import db
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Addproduct(db.Model):
    __searchable__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(80),  nullable=False)
    discount = db.Column(db.Integer(), default=0)
    stock = db.Column(db.Integer(),  nullable=False)
    desc = db.Column(db.Text(180),  nullable=False)
    colors = db.Column(db.Text(180), unique=False, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False , default=datetime.utcnow)

    brand_id = db.Column(db.Integer , db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('posts', lazy=True))

    category_id = db.Column(db.Integer , db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False , default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False , default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False , default='image.jpg')

    def __repr__(self):
        return '<Addproduct %r>' % self.name



class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    categories = relationship('Category', backref='brand', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    brand_id = db.Column(db.Integer, ForeignKey('brand.id'), nullable=False)





