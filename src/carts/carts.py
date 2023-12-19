from flask import render_template,session, request,redirect,url_for,flash,current_app
from src import db , app
from flask_login import login_required , current_user , logout_user , login_user
from src.products.models import Addproduct
from src.products.routes import brands, catagories
from src.customers.model import CustomerOrder , Coupons
from flask_login import current_user
import json
import random
import string


coupon_code_discount = 0

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


# route responsible for Adding products to the shopping cart.
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        global coupon_code_discount
        coupon_code_discount = 0
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method == "POST":
            DictItems = {
                product_id: {
                    'name': product.name,
                    'price': float(product.price),
                    'discount': product.discount,
                    'color': color,
                    'quantity': quantity,
                    'image': product.image_1,
                    'colors': product.colors
                }
            }
            # checking shoppingcart available in session
            if 'shoppingcart' in session:
                print(session['shoppingcart'])
                if product_id in session['shoppingcart']:
                    for key, item in session['shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['shoppingcart'] = MagerDicts(session['shoppingcart'], DictItems)
            else:
                session['shoppingcart'] = DictItems

            return redirect(url_for('home'))

    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('home'))


#route for Displaying the shopping cart.
@app.route('/carts')
def get_cart():
    global coupon_code_discount

    if 'shoppingcart' not in session or not session['shoppingcart'] or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))

    subtotal = 0
    total = 0
    grandtotal = 0

    # calculation the grandtotal
    for key, product in session['shoppingcart'].items():
        discount = (product['discount'] / 100) * float(product['price'])
        quantity = int(product['quantity']) if product['quantity'] is not None else 0
        subtotal += float(product['price']) * quantity
        subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        total = float("%.2f" % (1.06 * subtotal)) 
        grandtotal = round(total - coupon_code_discount, 2)


    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, brands=brands(), catagories=catagories())




#route which will help to Update the quantity and color of a product in the shopping cart.
@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!')
                    return redirect(url_for('get_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('get_cart'))


# delete the specific item from cart
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['shoppingcart'].items():
            if int(key) == id:
                session['shoppingcart'].pop(key, None)
                return redirect(url_for('get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('get_cart'))


# clear all the items in cart
@app.route('/clearcart')
def clearcart():
    try:
        session.pop('shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)



@login_required
def coupon_create():
    # Check if the user is logged in
    if not current_user.is_authenticated:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))


# this route will Generate and display a coupon code based on the user's order count.
@app.route('/coupon_create')
@login_required
def coupon_create():
    if not current_user.is_authenticated:
        flash('Please log in first', 'danger')
        return redirect(url_for('customerLogin'))
    # Check the order count for the current user
    order_count = CustomerOrder.query.filter_by(customer_id=current_user.id).count()

    # currently after every 3rd order you will get a discount coupon you can update the order count below to your requirement
    if order_count > 0 and order_count % 2 == 0:
        # Generate a unique coupon code
        coupon_code = generate_unique_coupon_code()

        # Insert the coupon code into the database
        coupon = Coupons(code=coupon_code, user_id=current_user.id)
        db.session.add(coupon)
        db.session.commit()

        flash('Congratulations! You are eligible for a 10% discount coupon.', 'success')
        flash(f'Your coupon code: {coupon_code}', 'info')
    else:
        flash("Sorry, no coupon code to redeem.", 'warning')

    return render_template('products/coupon.html')

def generate_unique_coupon_code():
    # Generate a random coupon code (6 characters, mixture of alphabet and numbers)
    coupon_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Ensure the generated code is unique by checking against the database
    while Coupons.query.filter_by(code=coupon_code).first() is not None:
        coupon_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    return coupon_code



# route which will help to Evaluate and apply the coupon code to the shopping cart.
@app.route('/cal_coupon', methods=['POST'])
def eval_coupon():
    global coupon_code_discount

    if request.method == 'POST':
        entered_coupon_code = request.form.get('couponCode')

        # Check if the entered coupon code exists in the database and belongs to the current user
        coupon = Coupons.query.filter_by(code=entered_coupon_code, user_id=current_user.id).first()

        if coupon:
            # Coupon code is valid, calculate the discount
            subtotal = 0
            grandtotal = 0

            for key, product in session.get('shoppingcart', {}).items():
                discount = (product['discount'] / 100) * float(product['price'])
                quantity = int(product['quantity']) if product['quantity'] is not None else 0
                subtotal += float(product['price']) * quantity
                subtotal -= discount
                tax = float("%.2f" % (0.06 * subtotal))
                grandtotal = float("%.2f" % (1.06 * subtotal))

                discount_amount = 0.10 * grandtotal
                coupon_code_discount = discount_amount
                session['coupon_code_discount'] = discount_amount


            flash(f'Coupon code applied successfully! You got an extra 10% discount.', 'success')
            flash(f'Discount amount: {discount_amount:.2f}', 'info')
        else:
            flash('Invalid coupon code or the coupon does not belong to you. Please try again.', 'danger')

    return redirect(url_for('get_cart'))
