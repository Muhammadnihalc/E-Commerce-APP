from flask import render_template , session , request , redirect , url_for , flash , Blueprint
from src import app, db , bcrypt
from .forms import CustomerRegisterForm
from .model import Register
from src.products.models import Addproduct , Brand ,Category
from flask import g
import os


@app.route('/user/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    if request.method == 'POST':
        hash_Password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_Password, country= form.Country.data , state = form.state.data , city = form.city.data , address = form.address.data , zipcode = form.zipcode.data)
        db.session.add(register)
        flash(f'welcome {form.name.data} Thankyou for registering' , 'success')
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('customer/register.html', form=form)