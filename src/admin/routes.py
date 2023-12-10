from flask import render_template , session , request , redirect , url_for , flash , Blueprint
from src import app, db , bcrypt
from .forms import RegistrationForm , Loginforms
from .models import User
from src.products.models import Addproduct , Brand ,Category
from flask import g
import os


@app.route('/admin')
def admin_home():
    if not g.logged_in:
        flash('please login first', 'danger')
        return redirect(url_for('login'))

    products = Addproduct.query.all()

    return render_template('admin/index.html', title='Admin page', products= products )


@app.route('/brands')
def brands_home():
    if not g.logged_in:
        flash('please login first', 'danger')
        return redirect(url_for('login'))
    
    brands = Brand.query.order_by(Brand.id.desc().all())

    return render_template('admin/brand.html', title='brand page', brands= brands )


@app.route('/category')
def category():
    if not g.logged_in:
        flash('please login first', 'danger')
        return redirect(url_for('login'))
    
    Categories = category.query.order_by(category.id.desc().all())

    return render_template('admin/brand.html', title='brand page', Categories= categories )



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_Password = bcrypt.generate_password_hash(form.password.data)
        user = User(Name=form.name.data, username=form.username.data, email=form.email.data, password=hash_Password)
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
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
            session['logged_in'] = True
            flash(f'welcome {form.email.data} ')
            return redirect(url_for('home'))
            #return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('invalid credentials ', 'danger')
    
    return render_template('admin/login.html', form=form, title="Login Page")
