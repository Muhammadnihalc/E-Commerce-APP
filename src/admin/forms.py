from wtforms import Form, BooleanField, StringField, PasswordField, validators

#form for admin registration
class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    # requesting special code for admin registration preventing outside users from admin registration
    company_secret_code = StringField('Company Secret Code', [validators.DataRequired(), validators.Length(min=8, max=20)])

#form for admin login
class Loginforms(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired()])