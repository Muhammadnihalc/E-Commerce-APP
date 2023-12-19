from flask import redirect , render_template , url_for , flash , request, session , current_app
from src import db , app #, whoosh_index
from .models import Brand , Category , Addproduct
import secrets , os
from .forms import Addproducts 
from flask import session
from src.helpers import save_image
from werkzeug.utils import secure_filename
from sqlalchemy import or_


# below fun() will help to Query for retrieving all brands associated with existing products
def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands


# this fun() will help in Query to retrieve all categories associated with existing products
def catagories():
    catagories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return catagories

# home page 
@app.route('/')
def home():
    # Get the page parameter from the request, defaulting to 1 if not provided
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)

    # Check if there are no products
    if not products.items:
        flash("Sorry, admin has not added any products. You can browse and purchase the products once the admin adds them.", 'info')

    return render_template('products/index.html', products=products, brands=brands(), categories=catagories())



# this route helps in searching 
@app.route('/result')
def result():
    search_query = request.args.get('q')

    if search_query:
        # Perform the search only if a search term is provided
        products = Addproduct.query.filter(
            or_(
                Addproduct.name.ilike(f"%{search_query}%"),
                Addproduct.desc.ilike(f"%{search_query}%")
            )
        ).limit(6).all()
    else:
        # If no search term is provided, return an empty list
        products = []

    return render_template('products/result.html', products=products, brands=brands(), categories=catagories())




@app.route('/session')
def session_check():
    for key, value in session.items():
        return(f'{key}: {value}')
    

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('home'))


# this route will Retrieve a single product by its ID or return a 404 error if not found
@app.route('/product/<int:id>')
def single_page(id):  
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html', product=product, brands=brands(), categories=catagories())


 # Retrieve products associated with the specified brand
@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
    return render_template('products/index.html',brand=brand,brands=brands(),catagories=catagories(),get_brand=get_brand)

 # Retrieve products associated with the specified category
@app.route('/categories/<int:id>')
def get_category():
    page = request.args.get('page',1,type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_prod= Addproduct.query.filter_by(category= get_cat).paginate(page=page , per_page = 4)
  
    return render_template('products/index.html' , get_prod=get_prod , categories=catagories(), brands=brands() , get_cat=get_cat)


# route to add new brand
@app.route('/addbrand', methods = ['GET', 'POST'])
def addbrand():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added' , 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands= 'brands')


# route to add new category
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        getcat = request.form.get('category')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'The category {getcat} was added', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))

    return render_template('products/addbrand.html')


# edit an excisting brand
@app.route('/editbrand/<int:id>', methods=['GET', 'POST'])
def editbrand(id):
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    brand = Brand.query.get_or_404(id)

    if request.method == 'POST':
        brand.name = request.form.get('brand')
        db.session.commit()
        flash(f'The brand {brand.name} was updated', 'success')
        return redirect(url_for('editbrand', id=brand.id))

    return render_template('products/editbrand.html', brand=brand)

# delete a specific brand and all products associated with it
@app.route("/deletebrand/<int:id>", methods=['POST'])
def deletebrand(id):
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    brand = Brand.query.get_or_404(id)

    try:
        db.session.delete(brand)
        db.session.commit()
        flash('Brand and its associated products has been deleted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting the brand: ' + str(e), 'danger')

    return redirect(url_for('admin_home'))



#edit an excisting category
@app.route('/editcategory/<int:id>', methods=['GET', 'POST'])
def editcategory(id):
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    category = Category.query.get_or_404(id)

    if request.method == 'POST':
        category.name = request.form.get('category')
        db.session.commit()
        flash(f'The category {category.name} was updated', 'success')
        return redirect(url_for('editcategory', id=category.id))

    return render_template('products/editcategory.html', category=category)

#  delete a specific category and all products associated with it
@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    
    category = Category.query.get_or_404(category_id)

    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category and its associated products deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting the category: {str(e)}', 'error')

    return redirect(url_for('admin_home'))

#add a new product
@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    brands = Brand.query.all()
    categories = Category.query.all()

    form = Addproducts(request.form)

    if request.method == 'POST':
        try:
            name = form.name.data
            price = form.price.data
            discount = form.discount.data
            stock = form.stock.data
            colors = form.colors.data
            desc = form.discription.data
            brand = request.form.get('brand')
            category = request.form.get('category')

            image_1 = save_image(request.files.get('image_1'))
            image_2 = save_image(request.files.get('image_2'))
            image_3 = save_image(request.files.get('image_3'))

            addpro = Addproduct(
                name=name, price=price, discount=discount, stock=stock, colors=colors,
                desc=desc, brand_id=brand, category_id=category,
                image_1=image_1, image_2=image_2, image_3=image_3
            )

            db.session.add(addpro)
            flash(f'The product {name} was added', 'success')
            db.session.commit()
            return redirect(url_for('admin_home'))

        except Exception as e:
            flash('verify the uploaded images are in valid format like jpeg,png ,jpg etc... ', 'danger')
            return redirect(url_for('add_product'))

    return render_template('products/addproduct.html', title="Add product", form=form, brands=brands, categories=categories)


# update the specific product
@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)

    # Change this line
    selected_category = request.form.get('category')

    brand = request.form.get('brand')
    form = Addproducts(request.form)

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.discription = form.discription.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = save_image(request.files.get('images_1'), name=secrets.token_hex(16) + ",")
            except:
                product.image_1 = save_image(request.files.get('images_1'), name=secrets.token_hex(16) + ",")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = save_image(request.files.get('images_2'), name=secrets.token_hex(16) + ",")
            except:
                product.image_2 = save_image(request.files.get('images_2'), name=secrets.token_hex(16) + ",")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = save_image(request.files.get('images_3'), name=secrets.token_hex(16) + ",")
            except:
                product.image_3 = save_image(request.files.get('images_3'), name=secrets.token_hex(16) + ",")

        db.session.commit()
        flash('The product has been updated', 'success')
        return redirect(url_for('admin_home'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.discription.data = product.desc

    return render_template('products/updateproduct.html', title='Update Product Page', form=form, brand=brand,
                           categories=categories, product=product, brands=brands)



# delete a specific product
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    product = Addproduct.query.get_or_404(id)
    if request.method =='POST':
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_1))
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_2))
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_3))
            except Exception as e:
                print(e)


        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted' , 'success')
        return redirect(url_for('admin_home'))

    flash(f'The product cannot be deleted' , 'success')
    return redirect(url_for('admin_home'))
