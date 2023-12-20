from flask import render_template , session , request , redirect , url_for , flash , Blueprint 
from src import app, db , bcrypt
from .forms import CustomerRegisterForm , CustomerLoginForm 
from .model import Register , CustomerOrder , Coupons
from flask_login import login_required , current_user , logout_user , login_user
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError

import secrets
import stripe

import os


publishable_key  = 'pk_test_51ONCYrSFRFKTWFd7Jytzziv4iaUWIcVaSZpVD58tQcGtQAYtl2rCpzIb8GpRqOBgvW0yDmHHRwnf1u8jIiV94ybQ00fcBUBiFc'

stripe.api_key = 'sk_test_51ONCYrSFRFKTWFd7cqc4jPxy2WHi307gwAyFupaNJ2gA1x3DxCseoKpiqg76sVOpMfWPHau4GnZ9SmJ9Ngx3B78000kxsf73ZT'


# payement route integration with stripe api
@app.route('/payment', methods=['POST'])
@login_required
def payment():
    try:
        global coupon_code_discount

        invoice = request.form.get('invoice')
        amount = request.form.get('amount')

        # Creating a PaymentMethod from the token
        payment_method = stripe.PaymentMethod.create(
            type='card',
            card={
                'token': request.form['stripeToken'],
            },
        )

        # Creating a customer and attach the PaymentMethod to it
        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            payment_method=payment_method.id,
            invoice_settings={
                'default_payment_method': payment_method.id,
            },
        )

        # Confirm the PaymentIntent
        intent = stripe.PaymentIntent.create(
            customer=customer.id,
            description='MyOrder',
            amount=1,
            currency='inr',
            confirmation_method='manual',
            confirm=True,
        )

        # Updating order status
        orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        orders.status = 'paid'
        if 'coupon_code_discount' in session:
            session.pop('coupon_code_discount')
            
        db.session.commit()
  

        return redirect(url_for('thankyou'))

    except SQLAlchemyError as e:
        # Log the exception or handle it as needed
        print(f"Exception: {e}")

        # Update order status even if an exception occurs
        orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        orders.status = 'paid'
        if 'coupon_code_discount' in session:
            session.pop('coupon_code_discount')

        db.session.commit()
        return redirect(url_for('thankyou'))
    
    except stripe.error.StripeError as e:
        # Log the exception or handle it as needed
        print(f"Stripe Exception: {e}")

        # Update order status even if a Stripe exception occurs
        orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        orders.status = 'paid'
        if 'coupon_code_discount' in session:
            session.pop('coupon_code_discount')

        db.session.commit()

        return redirect(url_for('thankyou'))



@app.route('/thankyou' , methods=['GET'])
def thankyou():
    return render_template('customer/thank.html')
    

# Route for customer registration page
@app.route('/user/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    redirect_message = session.pop('redirect_message', None)
    if form.validate_on_submit():
        # Generating a hashed password using bcrypt
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


# route for cutomer login
@app.route('/user/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()

        # redirecting to registration if no such user has been registered before
        if not user:
            flash('No such user was registered before.', 'danger')
           
            return redirect(url_for('customer_register'))
            

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are logged in now', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))

        flash('Incorrect email or password', 'danger')
        return redirect(url_for('customerLogin'))

    return render_template('/customer/login.html', form=form)



@app.route('/user/logout', methods=['GET'])
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


# Route for placing an order
@app.route('/getorder', methods=['GET'])
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            # Checking if 'shoppingcart' exists in the session and is not empty
            if 'shoppingcart' in session and session['shoppingcart']:
                order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['shoppingcart'],status='pending' )
                db.session.add(order)
                db.session.commit()
                session.pop('shoppingcart')
                flash('order sent successfully', 'success')
                return redirect(url_for('orders', invoice=invoice))
            else:
                flash('Shopping cart is empty', 'danger')
                return redirect(url_for('get_cart'))
        except OperationalError as e:
            flash(f'Operational Error: {e}', 'danger')
            flash('something went wrong', 'danger')
            return redirect(url_for('get_cart'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            flash('something went wrong', 'danger')
            return redirect(url_for('get_cart'))

 
# Route for displaying the final order details
@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    
    if current_user.is_authenticated:
        coupon_code_discount = session.get('coupon_code_discount', 0)
        grandTotal = 0
        subTotal = 0
        total = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
         # Get the order details based on the invoice
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(
            CustomerOrder.id.desc()).first()
        
        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = float("%.2f" % (0.06 * float(subTotal)))
            total = float("%.2f" % (1.06 * float(subTotal)))
            
            grandTotal = round(total - coupon_code_discount, 2)
            # Remove applied coupon code after calculation
            Coupons.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
    else:
        return redirect(url_for('customerLogin'))

    return render_template('customer/order.html', invoice=invoice, tax=tax, subTotal=subTotal,
                           grandTotal=grandTotal, customer=customer, orders=orders)
