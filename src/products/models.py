from src import db
from datetime import datetime

# db model for adding products
class Addproduct(db.Model):
    __searchable__ = ['name', 'desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Foreign Key for Category model
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # Relationship with Category model
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))

    # Foreign Key for Brand model
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    # Relationship with Brand model
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')

    def __repr__(self):
        return '<Post %r>' % self.name

# db model for brands
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    # Relationship with product model
    products = db.relationship('Addproduct', backref='brand_relation', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return '<Brand %r>' % self.name

# db model for brands
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    # Relationship with product model
    products = db.relationship('Addproduct', backref='category_relation', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return '<Category %r>' % self.name
