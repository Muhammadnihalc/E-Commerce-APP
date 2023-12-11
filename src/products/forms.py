from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, StringField, validators, IntegerField, TextAreaField, DecimalField

def images_only(form, field):
    if field.data:
        if not any(field.data.filename.lower().endswith(allowed_ext) for allowed_ext in ['jpg', 'png', 'jpeg', 'gif']):
            raise validators.ValidationError('Images only.')

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])
    colors = TextAreaField('colors', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif']), images_only])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif']), images_only])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif']), images_only])
