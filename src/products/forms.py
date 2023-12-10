from flask_wtf.file import FileAllowed , FileField , FileRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators , IntegerField , TextAreaField , DecimalField

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])
    colors = TextAreaField('colors', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[ FileAllowed(['jpg', 'png', 'jpeg', 'gif']) , 'images only'])
    image_2 = FileField('Image 2', validators=[ FileAllowed(['jpg', 'png', 'jpeg', 'gif']) , 'images only'])
    image_3 = FileField('Image 3', validators=[ FileAllowed(['jpg', 'png', 'jpeg', 'gif']) , 'images only'])