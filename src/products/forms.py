from flask_wtf.file import FileAllowed , FileField , FileRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators , IntegerField , TextAreaField

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = IntegerField('price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])
    colors = TextAreaField('colors', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])