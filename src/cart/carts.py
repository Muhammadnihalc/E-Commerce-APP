from flask import redirect , render_template , url_for , flash , request, session , g , current_app
from src import db , app 
from src.products.models import Addproduct
from src.products.routes import brands , catagories
import json


def MergeDicts(dict1 , dict2):
    if isinstance(dict1 , list) and isinstance(dict2 , list):
        return dict1 + dict2
    
    elif isinstance(dict1 , dict) and isinstance(dict2 , dict):
        return dict(list(dict.items()) + list(dict2.items()))
    return False



@app.route('/addcart', methods = ['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and color and request.method == 'POST':
            DictItems = {product_id: {'name': product.name , 'price':product.price , 'discount':product.discount,'color':color, 'quantity':quantity , 'image':product.image_1}}
           
            if 'Shoppingcart' in session:
                print(session['shoppingcart'])
                if product_id in session['shoppingcart']:
                    for key.item in session['shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            items['quantity'] += 1
                
                else:
                    session['shoppingcart'] = MergeDicts(session['shoppingcart'], DictItems)
                    return redirect(request.referrer)


            else:
                session['shoppingcart'] = DictItems
                return redirect(request.referrer)


    except Exception as e:
        print(e)

    finally:
        return redirect(request.referrer)
    


@app.route('/Carts', methods = ['POST'])
def  get_cart():
    if 'Shoppingcart' in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    subtotal = 0
    grandtotal = 0

    for key.product in session['shoppingcart'].items():
        discount = (product ['discount']/100 + float(product['price']))
        subtotal += float(product['price']) * int(product['quantity'])
        tax = ("%0.2f" % (.06 * float(subtotal)))
        grandtotal = float("%0.2f" % (1.06 * subtotal))


    return render_template('products/carts.html' , tax=tax , grandtotal=grandtotal , brands=brands(), catagories=catagories())



@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    
    except Exception as e:
        print(e)


@app.route('/updatecart/<int:code>' , methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key)  == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('item updated')
                    return redirect(url_for('getcart'))

        except Exception as e:
            print(e)

        return redirect(url_for('getcart'))

    

@app.route('/deleteitem/<int:id>' , methods=['POST'])
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    try:
        session.modified = True
        for key.items in session['shoppingcart'].items():
            if int(key) == id:
                session['shoppingcart'].pop(key , None)
                return redirect(url_for('getcart'))
            

    

    except Exception as e:
        print(e)
        return redirect(url_for('get_cart'))
    

@app.route('/clearcart' , methods=['POST'])
def clearcart():
    try:
        session.pop('shoppingcart', None)
        return redirect(url_for('home'))
    
    except Exception as e:
        print(e)

    








    
    




   