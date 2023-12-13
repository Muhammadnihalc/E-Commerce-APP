from wtforms import Form , StringField , TextAreaField , PasswordField , SubmitField , validators
from flask_wtf.file import FileRequired , FileAllowed , FileField

class CustomerRegisterForm(Form):
    name = StringField('Name: ')
    username = StringField('Username', [validators.DataRequired() , validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.DataRequired() , validators.Email() ,validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password' ,[validators.DataRequired()])
    Country = StringField('Username', [validators.DataRequired() , validators.Length(min=4, max=25)])
    state = StringField('Username', [validators.DataRequired() , validators.Length(min=4, max=25)])
    city = StringField('Username', [validators.DataRequired() , validators.Length(min=4, max=25)])
    contact = StringField('Username', [validators.DataRequired() , validators.Length(min=4, max=25)])
    address = StringField('Username', [validators.DataRequired() , validators.Length(min=4, max=25)])
    zipcode = StringField('Username', [validators.DataRequired() , validators.Length(min=4, max=25)])

    profile = FileField('profile', validators=[FileAllowed(['jpg','png','jpeg','gif'])])

    submit = SubmitField('Register')