from flask import render_template , session , request , redirect , url_for , flash , Blueprint
from src import app, db , bcrypt
from .forms import RegistrationForm , Loginforms
from .models import User
import os


@app.route('/')
def admin_home():
    return render_template('admin/index.html', title='admin')

@app.route('/home')
def home():
    # Your home route logic here
    return "welcome"



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_Password = bcrypt.generate_password_hash(form.password.data)
        user = User(Name=form.name.data, username=form.username.data, email=form.email.data, password=hash_Password)
        db.session.add(user)
        db.session.commit()
        flash(f'welcome {form.name.data} Thanks for registering' , 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form , title = "Registration Page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Loginforms(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'welcome {form.email.data} ')
            return redirect(url_for('home'))
            #return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('invalid credentials ', 'danger')
    
    return render_template('admin/login.html', form=form, title="Login Page")
