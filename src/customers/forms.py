from wtforms import Form , StringField , TextAreaField , PasswordField , SubmitField , validators , ValidationError
from flask_wtf.file import FileRequired , FileAllowed , FileField
from flask_wtf import FlaskForm
from .model import Register

# Form for customer registration.
class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zip code: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Register')

    # Validate if the name is already in use.
    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    # Validate if the email address is already in use.    
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")

        

# Form for customer login.
class CustomerLoginForm(FlaskForm):
    email = StringField('Email Address:', [validators.DataRequired() , validators.Email()])
    password = PasswordField('Password:', [validators.DataRequired()])



    