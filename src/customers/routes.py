from flask import render_template , session , request , redirect , url_for , flash , Blueprint
from src import app, db , bcrypt
from .forms import CustomerRegisterForm , CustomerLoginForm
from .model import Register
from src.products.models import Addproduct , Brand ,Category
from flask import g
from flask_login import login_required , current_user , logout_user , login_user
import os


@app.route('/user/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_Password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_Password, country= form.Country.data , state = form.state.data , city = form.city.data , address = form.address.data , zipcode = form.zipcode.data)
        db.session.add(register)
        flash(f'welcome {form.name.data} Thankyou for registering' , 'success')
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('customer/register.html', form=form)


@app.route('/user/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user)
            flash('you are loged in now' , 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('customerLogin'))


    return render_template('/user/login.html', form=form)


@app.route('/user/logout', methods=['GET'])
def customer_logout():
    logout_user()
    logout_user(url_for('home'))