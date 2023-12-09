from flask import render_template ,  session , request , redirect , url_for , flash , Blueprint
from src import app, db , bcrypt
from .forms import RegistrationForm
from .models import User
import os


@app.route('/')
def admin_home():
    return render_template('admin/index.html', title='admin')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_Password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email = form.email.data,
                   password = hash_Password)
        db.session.add(user)
        db.session.commit()
        flash(f'welcome {form.name.data} Thanks for registering' , 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form , title = "Registration Page")

