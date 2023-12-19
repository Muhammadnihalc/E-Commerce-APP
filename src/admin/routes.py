from flask import render_template , session , request , redirect , url_for , flash , Blueprint
from src import app, db , bcrypt
from .forms import RegistrationForm , Loginforms
from .models import User
from src.products.models import Addproduct , Brand ,Category
import os


#Admin home route which Displays all the list of products.
@app.route('/admin')
def admin_home():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    

    products = Addproduct.query.all()

    return render_template('admin/index.html', title='Admin page', products= products )


#Brands  route which will displays all the available list of brands.
@app.route('/brands')
def brands_home():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
  
    
    brands = Brand.query.order_by(Brand.id.desc()).all()

    return render_template('admin/brand.html', title='brand page', brands= brands )


#category  route which will displays all the available list of category.
@app.route('/category')
def category():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    Categories = Category.query.order_by(Category.id.desc()).all()

    return render_template('admin/brand.html', title='brand page', Categories=Categories )


# Registration route which will handles admin registration.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # checking the secret code preventing outside users from admin registration 
        if form.company_secret_code.data == 'secret123':
            hash_Password = bcrypt.generate_password_hash(form.password.data)
            user = User(Name=form.name.data, username=form.username.data, email=form.email.data, password=hash_Password)
            db.session.add(user)
            db.session.commit()
            session['logged_in'] = True
            flash(f'welcome {form.name.data} Thanks for registering' , 'success')
            return redirect(url_for('admin_home'))
        else:
            flash('Invalid company secret code', 'danger')
            
    return render_template('admin/register.html', form=form , title = "Registration Page")

# admin login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Loginforms(request.form)
    if request.method == 'POST' and form.validate():
        # redirecting to registration if no such user has been registered before
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session['email'] = form.email.data
                session['logged_in'] = True
                flash(f'Welcome {form.email.data}')
                return redirect(url_for('admin_home'))
            else:
                flash('Invalid credentials - wrong password', 'danger')
        else:
            flash('No such user has been registered. Please register.', 'danger')
            return redirect(url_for('register'))

    return render_template('admin/login.html', form=form, title="Login Page")


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('email', None)
        session.pop('logged_in', None)

        flash('You have been logged out', 'success')
    else:
        flash('You are not logged in', 'warning')

    return redirect(url_for('admin_home'))
