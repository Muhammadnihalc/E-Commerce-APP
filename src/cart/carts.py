from flask import redirect , render_template , url_for , flash , request, session , g , current_app
from src import db , app 
from src.products.models import Addproduct


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
                    print("This product is already in your cart")
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

   